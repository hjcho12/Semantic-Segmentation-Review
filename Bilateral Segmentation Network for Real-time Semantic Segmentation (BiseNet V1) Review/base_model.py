import torch.nn as nn


class CBR(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super(CBR, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x

class SeparableConvBnRelu(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=1, stride=1,
                 padding=0, dilation=1,
                 has_relu=True, norm_layer=nn.BatchNorm2d):
        super(SeparableConvBnRelu, self).__init__()

        self.conv1 = nn.Conv2d(in_channels, in_channels, kernel_size, stride,
                               padding, dilation, groups=in_channels,
                               bias=False)
        self.point_wise_cbr = CBR(in_channels, out_channels, 1, 1, 0)

    def forward(self, x):
        x = self.conv1(x)
        x = self.point_wise_cbr(x)
        return x


class Block(nn.Module):
    expansion = 4

    def __init__(self, in_channels, mid_out_channels, has_proj, stride,
                 dilation=1, norm_layer=nn.BatchNorm2d):
        super(Block, self).__init__()
        self.has_proj = has_proj

        if has_proj:
            self.proj = SeparableConvBnRelu(in_channels,
                                            mid_out_channels * self.expansion,
                                            3, stride, 1,
                                            has_relu=False,
                                            norm_layer=norm_layer)

        self.residual_branch = nn.Sequential(
            SeparableConvBnRelu(in_channels, mid_out_channels,
                                3, stride, dilation, dilation,
                                has_relu=True, norm_layer=norm_layer),
            SeparableConvBnRelu(mid_out_channels, mid_out_channels, 3, 1, 1,
                                has_relu=True, norm_layer=norm_layer),
            SeparableConvBnRelu(mid_out_channels,
                                mid_out_channels * self.expansion, 3, 1, 1,
                                has_relu=False, norm_layer=norm_layer))
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        shortcut = x
        if self.has_proj:
            shortcut = self.proj(x)

        residual = self.residual_branch(x)
        output = self.relu(shortcut + residual)

        return output


class Xception(nn.Module):
    def __init__(self, block, layers, channels, norm_layer=nn.BatchNorm2d):
        super(Xception, self).__init__()

        self.in_channels = 8
        self.conv1 = CBR(3, self.in_channels, 3, 2, 1)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(block, norm_layer,
                                       layers[0], channels[0], stride=2)
        self.layer2 = self._make_layer(block, norm_layer,
                                       layers[1], channels[1], stride=2)
        self.layer3 = self._make_layer(block, norm_layer,
                                       layers[2], channels[2], stride=2)

    def _make_layer(self, block, norm_layer, blocks,
                    mid_out_channels, stride=1):
        layers = []
        has_proj = True if stride > 1 else False
        layers.append(block(self.in_channels, mid_out_channels, has_proj,
                            stride=stride, norm_layer=norm_layer))
        self.in_channels = mid_out_channels * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.in_channels, mid_out_channels,
                                has_proj=False, stride=1,
                                norm_layer=norm_layer))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.maxpool(x)

        blocks = []
        x = self.layer1(x)
        blocks.append(x)
        x = self.layer2(x)
        blocks.append(x)
        x = self.layer3(x)
        blocks.append(x)

        return blocks


def xception39():
    model = Xception(Block, [4, 8, 4], [16, 32, 64])
    return model