import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
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

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateSeller: Prisma.SellerUpdateInput) {
    return this.sellerService.update(+id, updateSeller);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.sellerService.remove(+id);
  }
}
