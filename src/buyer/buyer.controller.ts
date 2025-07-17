import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { BuyerService } from './buyer.service';
import { Prisma } from 'generated/prisma';

@Controller('buyer')
export class BuyerController {
  constructor(private readonly buyerService: BuyerService) {}

  @Post()
  create(@Body() createBuyer: Prisma.BuyerCreateInput) {
    return this.buyerService.create(createBuyer);
  }

  @Get()
  findAll() {
    return this.buyerService.findAll();
  }

  @Get(':email')
  findByEmail(@Param('email') email: string) {
    return this.buyerService.findByEmail(email);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.buyerService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateBuyer: Prisma.BuyerUpdateInput) {
    return this.buyerService.update(+id, updateBuyer);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.buyerService.remove(+id);
  }
}
