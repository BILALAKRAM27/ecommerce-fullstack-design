import { Controller, Get, Post, Body, Patch, Param, Delete, HttpException, HttpStatus, Put } from '@nestjs/common';
import { SellerService } from './seller.service';
import { Prisma } from 'generated/prisma';



@Controller('seller')
export class SellerController {
  constructor(private readonly sellerService: SellerService) {}

  @Post()
  create(@Body() createSeller: Prisma.SellerCreateInput) {
    return this.sellerService.create(createSeller);
  }

  @Get()
  findAll() {
    return this.sellerService.findAll();
  }

  @Get(':email')
  findOne(@Param('email') email: string) {
    return this.sellerService.findOne(email);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() updateSeller: Prisma.SellerUpdateInput) {
    try {
      return await this.sellerService.update(+id, updateSeller);
    } catch (error) {
      if (error.code === 'P2002') { // Prisma unique constraint failed
        throw new HttpException(`Duplicate value for unique field: ${error.meta?.target?.join(', ') || 'unknown'}`, HttpStatus.BAD_REQUEST);
      }
      throw new HttpException(error.message || 'Update failed', HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.sellerService.remove(+id);
  }
}
