import os
import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchvision import datasets

from fanogan.test_anomaly_detection import test_anomaly_detection

from model import Generator, Discriminator, Encoder
from tools import MVTecAD, MVTECAD_DATASET_NAMES


def main(opt):
    if type(opt.seed) is int:
        torch.manual_seed(opt.seed)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    mvtec_ad = MVTecAD()

    if not os.path.isdir(opt.dataset_name) or opt.force_download:
        mvtec_ad.download(opt.dataset_name)
        mvtec_ad.extract(opt.dataset_name)

    images = datasets.ImageFolder(f"./{opt.dataset_name}/test",
                                  transform=transforms.Compose(
                                    [transforms.Resize([opt.img_size]*2),
                                     transforms.RandomHorizontalFlip(),
                                     transforms.ToTensor(),
                                     transforms.Normalize([0.5, 0.5, 0.5],
                                                          [0.5, 0.5, 0.5])])
                                  )
    test_dataloader = DataLoader(images, batch_size=1, shuffle=False)

    generator = Generator(opt)
    discriminator = Discriminator(opt)
    encoder = Encoder(opt)

    test_anomaly_detection(opt, generator, discriminator, encoder,
                           test_dataloader, device)


"""
The code below is:
Copyright (c) 2018 Erik Linder-Norén
Licensed under MIT
(https://github.com/eriklindernoren/PyTorch-GAN/blob/master/LICENSE)
"""


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_name", type=str,
                        choices=MVTECAD_DATASET_NAMES,
                        help="name of MVTec Anomaly Detection Datasets")
    parser.add_argument("--force_download", "-f", action="store_true",
                        help="flag of force download")
    parser.add_argument("--latent_dim", type=int, default=100,
                        help="dimensionality of the latent space")
    parser.add_argument("--img_size", type=int, default=64,
                        help="size of each image dimension")
    parser.add_argument("--channels", type=int, default=3,
                        help="number of image channels")
    parser.add_argument("--seed", type=int, default=None,
                        help="value of a random seed")
    opt = parser.parse_args()

    main(opt)
