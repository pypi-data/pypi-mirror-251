from monai.data import decollate_batch
from monai.utils.enums import PostFix

from medlab.registry import TASKS, INFERERS, TRANSFORMS
from .base_task import BaseTask
import torch
import copy

@TASKS.register_module()
class BaseClsTask(BaseTask):
    def __init__(self, *args, **kwargs):
        """
        base classification task, one input, one output
        """
        super().__init__(*args, **kwargs)
        self.val_inferer = INFERERS.build(self.val_cfg.get('inferer', dict(type='SimpleInferer')))
        self.test_inferer = INFERERS.build(self.test_cfg.get('inferer', dict(type='SimpleInferer')))
        num_classes = kwargs.get('num_classes', None)
        assert num_classes is not None, "num_classes must be specified in model"
        if num_classes == 1:
            self.post_pred_act = TRANSFORMS.build([
                dict(type='ToDevice', device='cpu'),
                dict(type='Activations', sigmoid=True)
            ])
            self.post_pred_cls = TRANSFORMS.build([
                dict(type='AsDiscrete', threshold=0.5)
            ])
            self.post_label = TRANSFORMS.build([dict(type='ToDevice', device='cpu')])

            post_save = []
        else:
            self.post_pred_act = TRANSFORMS.build([
                dict(type='ToDevice', device='cpu'),
                dict(type='Activations', softmax=True)
            ])

            self.post_pred_cls = TRANSFORMS.build([
                dict(type='AsDiscrete', argmax=True, to_onehot=num_classes),
            ])
            self.post_label = TRANSFORMS.build([
                dict(type='AsDiscrete', to_onehot=num_classes),
                dict(type='ToDevice', device='cpu')
            ])
            post_save = [
                dict(type='AsDiscreted', keys='preds', argmax=True)
            ]
        save_dir = self.test_cfg.get('save_dir', None)
        if save_dir is not None:
            post_save.extend([
                dict(
                    type='CopyItemsd',
                    keys=PostFix.meta("images"),
                    times=1,
                    names=PostFix.meta("preds")
                ),
                dict(
                    type='SaveClassificationd',
                    keys='preds',
                    saver=None,
                    meta_keys=None,
                    output_dir=save_dir,
                    filename='predictions.csv',
                    delimiter=",",
                    overwrite=True)
            ])
        self.post_save = TRANSFORMS.build(post_save)

        self.train_metrics_key = copy.deepcopy(self.metrics_key)
        self.train_metrics = copy.deepcopy(self.metrics)

        self.val_metrics_key = copy.deepcopy(self.metrics_key)
        self.val_metrics = copy.deepcopy(self.metrics)

        if 'ROCAUCMetric' in self.metrics_key:
            index_train = self.train_metrics_key.index('ROCAUCMetric')
            index_val = self.train_metrics_key.index('ROCAUCMetric')
            self.train_metrics_key.pop(index_train)
            self.val_metrics_key.pop(index_val)
            self.train_roc_auc_metric = self.train_metrics.pop(index_train)
            self.val_roc_auc_metric = self.val_metrics.pop(index_val)
        else:
            self.train_roc_auc_metric = None
            self.val_roc_auc_metric = None

        self.training_step_loss = []
        self.validation_step_loss = []

    def forward(self, x):
        return self._model(x)

    def training_step(self, batch, batch_idx):
        """
        training step for classification task
        :param batch: batch data
        :param batch_idx: batch index
        :return: loss
        """
        images = batch['images']
        labels = batch['labels']

        batch_size = images.shape[0]
        outputs = self.forward(images)


        loss = self.loss_func(outputs, labels)

        if isinstance(outputs, (tuple, list)):
            outputs = outputs[0]

        outputs = [self.post_pred_act(i) for i in decollate_batch(outputs)]
        labels = [self.post_label(i) for i in decollate_batch(labels)]

        if self.train_roc_auc_metric is not None:
            self.train_roc_auc_metric(outputs, labels)
        
        outputs = [self.post_pred_cls(i) for i in outputs]

        if len(self.train_metrics) > 0:
            for metric in self.train_metrics:
                metric(outputs, labels)

        self.training_step_loss.append(loss)

        # self.log("train_step_loss", loss.item(), sync_dist=True, batch_size=batch_size)
        return loss

    def on_train_epoch_end(self):
        self.log_dict(self.parse_train_metrics(), sync_dist=True)
        epoch_mean = torch.stack(self.training_step_loss).mean()
        self.log("train_loss", epoch_mean.item(), sync_dist=True)
        self.training_step_loss.clear()

    def validation_step(self, batch, batch_idx):
        """
        validation step for classification task
        :param batch: batch data
        :param batch_idx: batch index
        :return: None
        """
        images = batch['images']
        labels = batch['labels']

        batch_size = images.shape[0]
        outputs = self.val_inferer(inputs=images, network=self.forward)

        loss = self.loss_func(outputs, labels)


        if isinstance(outputs, (tuple, list)):
            outputs = outputs[0]

        outputs = [self.post_pred_act(i) for i in decollate_batch(outputs)]
        labels = [self.post_label(i) for i in decollate_batch(labels, detach=False)]

        if self.val_roc_auc_metric is not None:
            self.val_roc_auc_metric(outputs, labels)

        outputs = [self.post_pred_cls(i) for i in outputs]

        if len(self.val_metrics) > 0:
            for metric in self.val_metrics:
                metric(outputs, labels)
        
        self.validation_step_loss.append(loss)

        # self.log('val_step_loss', loss.item(), sync_dist=True, batch_size=batch_size)

    def on_validation_epoch_end(self):
        """
        validation epoch end hook, parse and log metrics
        """
        self.log_dict(self.parse_val_metrics(), sync_dist=True)
        epoch_mean = torch.stack(self.validation_step_loss).mean()
        self.log("val_loss", epoch_mean.item(), sync_dist=True)
        self.validation_step_loss.clear()


    def test_step(self, batch, batch_idx):
        """
        test step for classification task, save predictions to csv file
        :param batch: batch data
        :param batch_idx: batch index
        :return:
        """
 
        images = batch["images"]
        labels = batch["labels"]

        outputs = self.test_inferer(inputs=images, network=self.forward)

        if isinstance(outputs, (tuple, list)):
            outputs = outputs[0]

        batch["preds"] = outputs

        outputs = [self.post_pred_act(i) for i in decollate_batch(outputs)]
        labels = [self.post_label(i) for i in decollate_batch(labels)]

        if self.roc_auc_metric is not None:
            self.roc_auc_metric(outputs, labels)

        outputs = [self.post_pred_cls(i) for i in outputs]

        if len(self.metrics) > 0:
            for metric in self.metrics:
                metric(outputs, labels)

        for i in decollate_batch(batch):
            self.post_save(i)

    def on_test_epoch_end(self):
        """
        test epoch end hook, parse metrics
        """
        print(self.parse_metrics())

    def parse_train_metrics(self):
        """
        parse metrics to dict
        :return: metrics dict
        """
        value_dict = {}
        values = []
        if self.train_roc_auc_metric is not None:
            value_dict['ROCAUCMetric'] = self.train_roc_auc_metric.aggregate()
            self.train_roc_auc_metric.reset()

        for metric in self.train_metrics:
            value = metric.aggregate()

            if isinstance(value, list):
                values.extend([v.item() for v in value])
            else:
                values.append(value.item())
        value_dict.update(dict(zip(self.train_metrics_key, values)))

        for metric in self.metrics:
            metric.reset()
        
        value_dict = {f'train_{k}': v for k, v in value_dict.items()}

        return value_dict

    def parse_val_metrics(self):
        """
        parse metrics to dict
        :return: metrics dict
        """
        value_dict = {}
        values = []
        if self.val_roc_auc_metric is not None:
            value_dict['ROCAUCMetric'] = self.val_roc_auc_metric.aggregate()
            self.val_roc_auc_metric.reset()

        for metric in self.val_metrics:
            value = metric.aggregate()

            if isinstance(value, list):
                values.extend([v.item() for v in value])
            else:
                values.append(value.item())
        value_dict.update(dict(zip(self.val_metrics_key, values)))

        for metric in self.metrics:
            metric.reset()
        
        value_dict = {f'val_{k}': v for k, v in value_dict.items()}

        return value_dict