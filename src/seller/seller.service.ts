import { ForbiddenException, Injectable, NotFoundException } from '@nestjs/common';
import { DatabaseService } from 'src/database/database.service';
import { Prisma } from 'generated/prisma';

@Injectable()
export class SellerService {
  constructor(private readonly databaseService: DatabaseService) {}

  async getSellerProfile(id: number) {
    return this.databaseService.seller.findUnique({
      where: {
        seller_id: id,
      },
    });
  }

  async updateseller(id: number, updateSeller: Prisma.SellerUpdateInput) {
    return this.databaseService.seller.update({
      where: { seller_id: id },
      data: updateSeller,
    });
  }

  async CreateProduct(user_id: number, createProduct: {
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
    const seller = await this.databaseService.seller.findUnique({
      where: { user_id: user_id },
    });
    if (!seller) {
      throw new Error('only sellers can add the products');
    }

    const finalPrice = createProduct.base_price - (createProduct.base_price * (createProduct.discount_percentage || 0) / 100);

    const productData: any = {
      seller_id: seller.seller_id,
      name: createProduct.name,
      description: createProduct.description,
      base_price: createProduct.base_price,
      discount_percentage: createProduct.discount_percentage,
      final_price: finalPrice,
      category_id: createProduct.category_id,
      condition: createProduct.condition,
      stock: createProduct.stock,
    };

    if (createProduct.brand_id) {
      productData.brand_id = createProduct.brand_id;
    }

    if (createProduct.images) {
      productData.images = {
        create: createProduct.images.map((url: string) => ({ image_url: url })),
      };
    }

    if (createProduct.attributes) {
      productData.attributeValues = {
        create: createProduct.attributes.map((attr: any) => ({
          attribute_id: attr.attribute_id,
          value: attr.value,
        }))
      };
    }

    return this.databaseService.product.create({
      data: productData,
    });
  }

  async getProducts(seller_id: number) {
    const seller = await this.databaseService.seller.findUnique({
      where: { seller_id: seller_id },
    });
    if (!seller) {
      throw new Error('Seller not found');
    }
    return this.databaseService.product.findMany({
      where: {
        seller_id: seller.seller_id,
      },
      include: {
        images: true, 
        attributeValues: {
          include: {
            attribute: true
          }
        }, 
        category: true, 
        brand: true
      },
    });
  }

  async getProduct(product_id: number, userId: number) {
    const product = await this.databaseService.product.findUnique({
      where: { product_id: product_id },
      include: {
        images: true, 
        attributeValues: {
          include: {
            attribute: true
          }
        }, 
        category: true, 
        brand: true
      },
    });
    if (!product) throw new NotFoundException('Product not found.');

    const seller = await this.databaseService.seller.findUnique({ where: { user_id: userId } });
    if (product.seller_id !== seller?.seller_id) {
      throw new ForbiddenException('Access denied.');
    }
    return product;
  }

  async updateProduct(productId: number, userId: number, updateProduct: any) {
    const seller = await this.databaseService.seller.findUnique({ where: { user_id: userId } });
    const product = await this.databaseService.product.findUnique({ where: { product_id: productId } });

    if (!product || product.seller_id !== seller?.seller_id) {
      throw new ForbiddenException('You can only update your own products.');
    }

    await this.databaseService.productImage.deleteMany({ where: { product_id: productId } });
    await this.databaseService.productAttributeValue.deleteMany({ where: { product_id: productId } });

    const finalPrice = updateProduct.base_price ? 
      updateProduct.base_price - (updateProduct.base_price * (updateProduct.discount_percentage || 0) / 100) : 
      undefined;

    return this.databaseService.product.update({
      where: { product_id: productId },
      data: {
        ...updateProduct,
        final_price: finalPrice,
        images: updateProduct.images ? {
          create: updateProduct.images.map((url: string) => ({ image_url: url })),
        } : undefined,
        attributeValues: updateProduct.attributes ? {
          create: updateProduct.attributes.map((attr: any) => ({
            attribute: {
              connect: { attribute_id: attr.attribute_id }
            },
            value: attr.value,
          })),
        } : undefined,
      },
    });
  }

  async deleteProduct(productId: number, userId: number) {
    const seller = await this.databaseService.seller.findUnique({ where: { user_id: userId } });
    const product = await this.databaseService.product.findUnique({ where: { product_id: productId } });

    if (!product || product.seller_id !== seller?.seller_id) {
      throw new ForbiddenException('You can only delete your own products.');
    }

    return this.databaseService.product.delete({ where: { product_id: productId } });
  }
}
  

  

