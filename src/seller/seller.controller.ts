import { 
  Controller, 
  Get, 
  Post, 
  Put, 
  Delete, 
  Body, 
  Param, 
  UseGuards, 
  Req,
  HttpCode,
  HttpStatus,
  ParseIntPipe
} from '@nestjs/common';
import { SellerService } from './seller.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('seller')
@UseGuards(JwtAuthGuard)
export class SellerController {
  constructor(private readonly sellerService: SellerService) {}

  // Get seller profile
  @Get('profile')
  @HttpCode(HttpStatus.OK)
  async getSellerProfile(@Req() req) {
    const userId = req.user.userId;
    const seller = await this.sellerService.getSellerProfile(userId);
    if (!seller) {
      throw new Error('Seller profile not found');
    }
    return seller;
  }

  // Update seller profile
  @Put('profile')
  @HttpCode(HttpStatus.OK)
  async updateSellerProfile(@Req() req, @Body() updateData: any) {
    const userId = req.user.userId;
    const seller = await this.sellerService.getSellerProfile(userId);
    if (!seller) {
      throw new Error('Seller profile not found');
    }
    return this.sellerService.updateseller(seller.seller_id, updateData);
  }

  // Create a new product
  @Post('products')
  @HttpCode(HttpStatus.CREATED)
  async createProduct(@Req() req, @Body() createProductData: {
    name: string;
    description?: string;
    base_price: number;
    discount_percentage?: number;
    category_id: number;
    brand_id?: number;
    condition: 'new' | 'used' | 'refurbished';
    stock: number;
    images?: string[];
    attributes?: Array<{ attribute_id: number; value: string }>;
  }) {
    const userId = req.user.userId;
    return this.sellerService.CreateProduct(userId, createProductData);
  }

  // Get all products for the seller
  @Get('products')
  async getSellerProducts(@Req() req) {
    const userId = req.user.userId;
    const seller = await this.sellerService.getSellerProfile(userId);
    if (!seller) {
      throw new Error('Seller profile not found');
    }
    return this.sellerService.getProducts(seller.seller_id);
  }

  // Get a specific product by ID
  @Get('products/:productId')
  async getProduct(
    @Req() req,
    @Param('productId', ParseIntPipe) productId: number
  ) {
    const userId = req.user.userId;
    return this.sellerService.getProduct(productId, userId);
  }

  // Update a product
  @Put('products/:productId')
  @HttpCode(HttpStatus.OK)
  async updateProduct(
    @Req() req,
    @Param('productId', ParseIntPipe) productId: number,
    @Body() updateProductData: {
      name?: string;
      description?: string;
      base_price?: number;
      discount_percentage?: number;
      category_id?: number;
      brand_id?: number;
      condition?: 'new' | 'used' | 'refurbished';
      stock?: number;
      images?: string[];
      attributes?: Array<{ attribute_id: number; value: string }>;
    }
  ) {
    const userId = req.user.userId;
    return this.sellerService.updateProduct(productId, userId, updateProductData);
  }

  // Delete a product
  @Delete('products/:productId')
  @HttpCode(HttpStatus.NO_CONTENT)
  async deleteProduct(
    @Req() req,
    @Param('productId', ParseIntPipe) productId: number
  ) {
    const userId = req.user.userId;
    await this.sellerService.deleteProduct(productId, userId);
    return { message: 'Product deleted successfully' };
  }
}
