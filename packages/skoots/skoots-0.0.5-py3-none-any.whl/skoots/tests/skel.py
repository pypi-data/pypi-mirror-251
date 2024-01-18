import skimage.io as io
from skoots.lib.skeleton import skeleton_to_mask
from skoots.train.merged_transform import _get_affine_matrix, _get_inverse_affine_matrix, transform_from_cfg
import torch
from torch import Tensor
from torchvision.transforms.functional import affine
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
from skoots.config import get_cfg_defaults
import numpy as np

image = io.imread("/home/chris/Dropbox (Partners HealthCare)/skoots/tests/hide_test_2d.tif")
skeletons = {}
for u in np.unique(image):
    if u == 0: continue
    skel = skeletonize(image == u)
    skel = torch.from_numpy(skel).unsqueeze(-1).nonzero().round().float()
    skeletons[u] = skel


# x = torch.linspace(50, 200, 10).unsqueeze(1)
# y = torch.ones((10,1)) * 250/2
# z = torch.zeros((10,1))
#
# s = torch.concat((x,y,z), dim=1)

# unrotated_skeleton_mask = skeleton_to_mask(skeletons, (image.shape[0], image.shape[1], 1))

image = torch.from_numpy(image.astype(float)).unsqueeze(0).unsqueeze(-1)

# angle = torch.tensor((0))
# scale = torch.tensor((1))
# shear = torch.tensor((15))
# for s in range(1):
#     shear = torch.tensor((s)) + 15
#     mat: Tensor = _get_affine_matrix(
#         center=[image.shape[1] / 2, image.shape[2] / 2],
#         angle=angle.item(),
#         translate=[0.0, 0.0],
#         scale=scale.item(),
#         shear=[0.0, float(shear.item())],
#         device=str(image.device),
#     )
#
#
#     # print(mat / image.shape[1] / 2)
#     # _mat = _get_inverse_affine_matrix(
#     #     center=[image.shape[1] / 2, image.shape[2] / 2],
#     #     angle=-angle.item(),
#     #     translate=[0.0, 0.0],
#     #     scale=scale.item(),
#     #     shear=[float(shear.item()), float(shear.item())], #float(shear.item())],
#     #     inverted=False,
#     # )
#     # _mat += [0, 0, 1]
#     # _mat = torch.tensor(_mat).view(3,3)
#
#
#     # Rotate the skeletons by the affine matrix
#     for k, v in skeletons.items():
#         skeleton_xy = v[:, [0, 1]].permute(1, 0).unsqueeze(0)  # [N, 3] -> [1, 2, N]
#         _ones = torch.ones(
#             (1, 1, skeleton_xy.shape[-1]), device='cpu'
#         )  # [1, 1, N]
#         skeleton_xy = torch.cat((skeleton_xy, _ones), dim=1)  # [1, 3, N]
#         rotated_skeleton = mat @ skeleton_xy  # [1,3,N]
#         skeletons[k][:, [0, 1]] = rotated_skeleton[0, [0, 1], :].T.float()
#
#
#     rotated = skeleton_to_mask(skeletons, (image.shape[1], image.shape[2], 1))
#     rotated_image = affine(
#         image.permute(0, 3, 1, 2).float(),
#         angle=angle.item(),
#         shear=float(shear.item()),
#         scale=scale.item(),
#         translate=[0, 0],
#     ).permute(0, 2, 3, 1)

    # rotated_image[rotated > 0.5] = rotated_image.max() + 2
    # plt.imshow(rotated_image.squeeze().numpy())
    # plt.title('before')
    # plt.show()
    # plt.close()

def load_cfg_from_file(path):
    """Load configurations."""
    # Set configurations
    cfg = get_cfg_defaults()
    cfg.merge_from_file(path)
    cfg.freeze()
    return cfg


cfg = load_cfg_from_file('/home/chris/Dropbox (Partners HealthCare)/skoots-experiments/configs/mitochondria/test_fine_tune_skoots_on_all.yaml')

skeletons = {k:v.cuda() for k,v in skeletons.items()}

dd = {'image': image.cuda(), 'masks': image.cuda(), 'skeletons': skeletons}
for _ in range(1):
    out = transform_from_cfg(dd, cfg)
    rotated = skeleton_to_mask(out['skeletons'], (out['image'].shape[1], out['image'].shape[2], 1))
    out['image'][rotated > 0.5] = out['image'].max() + 2
    plt.imshow(out['image'].squeeze().cpu().numpy())
    plt.show()
    plt.close()


