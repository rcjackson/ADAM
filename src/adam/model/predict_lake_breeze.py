import torch

from huggingface_hub import hf_hub_download
from torch.nn import Identity 
from torchvision.models.segmentation import fcn_resnet50, deeplabv3_resnet50
from safetensors.torch import load_model
from scipy.ndimage import center_of_mass, label

from ..io import RadarImage

# Identity layer needed for the lake-breeze detector model
class Identity(torch.nn.Module):
    def __init__(self):
        super(Identity, self).__init__()

    def forward(self, x):
        return x

def infer_lake_breeze(radar_scan: RadarImage,
                    model_name='lakebreeze_best_model_deeplabv3_resnet50',
                    area_threshold=20):
    
    # Import our list of safe globals from PyTorch so that we only load weights in the model
    # This will prevent a malicious user from inserting malware into the pickle and having
    # ADAM execute that.

    if model_name == 'lakebreeze_model_fcn_resnet50_no_augmentation':
        model = fcn_resnet50(num_classes=2)
    elif model_name == 'lakebreeze_best_model_fcn_resnet50':
        model = fcn_resnet50(weights='FCN_ResNet50_Weights.COCO_WITH_VOC_LABELS_V1')
        in_channels = 2048
        inter_channels = 512
        channels = 2
        fcn_new_last_layer = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, inter_channels, 3, padding=1, bias=False),
            torch.nn.BatchNorm2d(inter_channels),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(inter_channels, channels, 1),
        )
        model.classifier = fcn_new_last_layer
        model.aux_classifier = Identity()
    elif model_name == "lakebreeze_best_model_deeplabv3_resnet50"
        model = deeplabv3_resnet50(weights='DeepLabV3_ResNet50_Weights.COCO_WITH_VOC_LABELS_V1')
        d_in_channels = 1024
        d_inter_channels = 256
        deeplab_new_last_layer = torch.nn.Sequential(
            torch.nn.Conv2d(d_in_channels, d_inter_channels, 3, padding=1, bias=False),
            torch.nn.BatchNorm2d(d_inter_channels),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv2d(d_inter_channels, channels, 1),
        )
        

    state_dict = hf_hub_download(repo_id="rcjackson/lakebreeze-resnet50",
            filename=f"https://huggingface.co/rcjackson/lakebreeze-resnet50/blob/main/{model_name}.safetensors")
    load_model(model, state_dict)
    image = RadarImage.pytorch_image
    mask = model(image)['out'].detach().numpy()
    mask = mask[0].argmax(axis=0)
    mask = mask.T
    
    # Filter out small regions that are not lake breezes
    labels, num_features = label(mask)
    largest_area = -99999
    largest_index = 0
    for i in range(num_features):
        area = mask[labels == i+1].sum()
        print(area)
        if area > largest_area:
            largest_area = area
            largest_index = i+1
        if area < area_threshold:
            mask[labels == i+1] = 0
    radar_scan.mask = mask
    return radar_scan
