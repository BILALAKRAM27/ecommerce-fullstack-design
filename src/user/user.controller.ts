import { Controller, Get, Post, Body, Patch, Param, Delete, Query } from '@nestjs/common';
import { UserService } from './user.service';
import { Prisma, Seller } from 'generated/prisma';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  create(@Body() createUser: Prisma.UserCreateInput) {
    return this.userService.create(createUser);
  }

  @Get()
  findAll(@Query("Role") Role?: 'seller' | 'buyer'|  'admin', @Query("Status") Status?: 'active' | 'suspended' | 'banned') {
    return this.userService.findAll(Role, Status); 
  }

  @Get(':id')
  findOne(@Param('email') email: string) {
    return this.userService.findOne(email);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateUser: Prisma.UserUpdateInput) {
    return this.userService.update(+id, updateUser);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.userService.remove(+id);
  }
}
