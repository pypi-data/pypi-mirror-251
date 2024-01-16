import torch
import torch.nn as nn


class TNetConvBlock(nn.Module):
    def __init__(self, input_size:int, output_size: int) -> None:
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size

        self.conv_block = nn.ModuleList([
            nn.Conv2d(self.input_size, self.output_size, 3, 1, padding="same"),
            nn.BatchNorm2d(self.output_size),
            nn.ReLU(),
            nn.Conv2d(self.output_size, self.output_size, 1, 1, padding="same"),
            nn.BatchNorm2d(self.output_size),
            nn.Conv2d(self.output_size, self.output_size, 3, 1, groups=self.output_size, padding="same"),
            nn.BatchNorm2d(self.output_size),
            nn.ReLU(),
            nn.MaxPool2d(2, stride=2, return_indices=True)
            ])
    def forward(self, x):
        output = []
        for layers in self.conv_block:
            x = layers(x)
            output.append(x)
        return output


class TNetConv1BnBlock(nn.Module):
    def __init__(self, input_size: int, output_size, stride_size: int = 2):
        super().__init__()
        self.conv = nn.Conv2d(input_size, output_size, stride=stride_size,kernel_size=1)
        self.bn = nn.BatchNorm2d(output_size)
    
    def forward(self, x):
        return self.bn(self.conv(x))


class TNetUpscaler(nn.Module):
    def __init__(self, input_size:int, output_size:int):
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size

        self.conv_block = nn.ModuleList([
            nn.Conv2d(self.input_size, self.output_size, 3, 1, padding="same"),
            nn.BatchNorm2d(self.output_size),
            nn.ReLU(),
            nn.Conv2d(self.output_size, self.output_size, 1, 1, padding="same"),
            nn.BatchNorm2d(self.output_size),
            nn.Conv2d(self.output_size, self.output_size, 3, 1, groups=2, padding="same"),
            nn.BatchNorm2d(self.output_size),
            nn.ReLU()])

    def forward(self, x):
        for layers in self.conv_block:
            x = layers(x)
        return x

    
class TNet(nn.Module):
    def __init__(self, input_channel = 3, emb_size:int = 512, num_classes:int = 3):
        super().__init__()
        self.input_conv = nn.Conv2d(in_channels=input_channel, out_channels=emb_size, kernel_size=3, padding="same")
        self.conv_block_1 = TNetConvBlock(input_size=emb_size, output_size=emb_size)
        self.conv_block_2 = TNetConvBlock(input_size=emb_size, output_size=int(emb_size//2))
        self.conv_block_3 = TNetConvBlock(input_size=int(emb_size//2), output_size=int(emb_size//4))

        self.conv1d_block_1 = TNetConv1BnBlock(input_size=emb_size, output_size=int(emb_size//2), stride_size=2)
        self.conv1d_block_2 = TNetConv1BnBlock(input_size=int(emb_size//2), output_size=int(emb_size//4), stride_size=2)

        self.residual_downsampler = lambda x,y: x + y[-1][0]
        
        
        # Upscaler Bloack
        self.conv_up_block1 = TNetUpscaler(input_size=int(emb_size//4), output_size=int(emb_size//4))
        self.unmax1 = nn.MaxUnpool2d(2, stride=2)
        self.conv1d_upscale1 = TNetConv1BnBlock(input_size=int(emb_size//4), output_size=int(emb_size//4), stride_size=1)

        self.conv_up_block2 = TNetUpscaler(input_size=int(emb_size//4), output_size=int(emb_size//4))
        self.unmax2 = nn.MaxUnpool2d(2, stride=2)
        self.conv1d_upscale2 = TNetConv1BnBlock(input_size=int(emb_size//4), output_size=int(emb_size//4), stride_size=1)
        
        self.conv_up_block3 = TNetUpscaler(input_size=int(emb_size//4), output_size=int(emb_size//2))
        self.unmax3 = nn.MaxUnpool2d(2, stride=2)
        self.conv1d_upscale3 = TNetConv1BnBlock(input_size=int(emb_size//4), output_size=int(emb_size//2), stride_size=1)

        self.conv_up_block4 = TNetUpscaler(input_size=int(emb_size//2), output_size=int(emb_size))
        self.conv1d_upscale4 = TNetConv1BnBlock(input_size=int(emb_size//2), output_size=int(emb_size), stride_size=1)

        self.output_conv = nn.Conv2d(in_channels=int(emb_size), out_channels=num_classes, kernel_size=3, stride=1, padding="same")
#         self.out = nn.Conv2d(in_channels=input_channel, out_channels=1, kernel_size=1)
        
        self.residual_upsampler = lambda x,y,z: x + y + z[-2] 
#         self.soft = nn.Sigmoid()

    def forward(self, x):
        x = self.input_conv(x)
        x = self.conv_block_1(x)
        
        # All shapes are as per 512 emb size if emb size changes, these values will change as well
        op_1d_conv = self.conv1d_block_1(x[-1][0]) # input -> shape (batch_size, 512, 128, 128) --> output -> shape (batch_size, 256, 64, 64)
        op_conv_blk2 = self.conv_block_2(x[-1][0]) # input -> shape (batch_size, 512, 128, 128) --> output -> shape (batch_size, 256, 64, 64)
        x1 = self.residual_downsampler(op_1d_conv, op_conv_blk2) # x1 -> shape (batch_size, 256, 64, 64)
        
        op_1d_conv2 = self.conv1d_block_2(x1) # input -> shape (batch_size, 256, 64, 64) --> output -> shape (batch_size, 128, 32, 32)
        op_conv_blk3 = self.conv_block_3(x1) # input -> shape (batch_size, 256, 64, 64) --> output -> shape (batch_size, 128, 32, 32)
        x2 = self.residual_downsampler(op_1d_conv2, op_conv_blk3) # x2 -> shape (batch_size, 128, 32, 32)


        # Upscaling operations
        up1 = self.conv_up_block1(x2) # input -> shape (batch_size, 128,32,32) --> output (batch_size, 128,32,32)
        up1_conv1d = self.conv1d_upscale1(x2) # input -> shape (batch_size, 128,32,32) --> output (batch_size, 128,32,32)
        up1 = up1 + up1_conv1d # up1 -> shape (batch_size, 128,32,32)
        up1 = self.unmax1(up1, indices=torch.ones_like(up1, dtype=torch.int64)) # input -> shape (batch_size, 128,32,32) --> output (batch_size, 128,64,64)

        up2 = self.conv_up_block1(up1) # input -> shape (batch_size, 128,64,64) --> output (batch_size, 128, 64, 64)
        up2_conv1d = self.conv1d_upscale2(up1) # input -> shape (batch_size, 128, 64, 64) --> output (batch_size, 128, 64, 64)
        up2 = self.residual_upsampler(up2, up2_conv1d, op_conv_blk3) # up2 -> shape (batch_size, 128, 64, 64)
        up2 = self.unmax2(up2, indices=torch.ones_like(up2, dtype=torch.int64)) # input -> shape (batch_size, 128, 64, 64) --> output (batch_size, 128, 128, 128)

        up3 = self.conv_up_block3(up2) # input -> shape (batch_size, 128,128,128) --> output (batch_size, 256, 128, 128)
        up3_conv1d = self.conv1d_upscale3(up2) # input -> shape (batch_size, 128, 128, 128) --> output (batch_size, 256, 128, 128)
        up3 = self.residual_upsampler(up3, up3_conv1d, op_conv_blk2) # up3 -> shape (batch_size, 256, 128, 128)
        up3 = self.unmax3(up3, indices=torch.ones_like(up3, dtype=torch.int64)) # input -> shape (batch_size, 256, 128, 128) --> output (batch_size, 256, 256, 256)

        up4 = self.conv_up_block4(up3) # input -> shape (batch_size, 256,256,256) --> output (batch_size, 512, 256, 256)
        up4_conv1d = self.conv1d_upscale4(up3) # input -> shape (batch_size, 512,256,256) --> output (batch_size, 512, 256, 256)
        up4 = self.residual_upsampler(up4, up4_conv1d, x) # up4 -> shape (batch_size, 512, 256, 256)


        output = self.output_conv(up4) # input -> shape (batch_size, 512, 256, 256) --> output (batch_size, 3, 512, 512)
        
#         return self.soft(self.out(output))
        return output
