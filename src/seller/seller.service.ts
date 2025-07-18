import * as bcrypt from 'bcrypt';
import { Injectable } from '@nestjs/common';
import { Prisma } from 'generated/prisma';
import { DatabaseService } from 'src/database/database.service';


@Injectable()
export class SellerService {
  constructor(private readonly database: DatabaseService) {}

  async create(createUser: Prisma.SellerCreateInput) {

    // Replace the plain password with the hashed one
    return this.database.seller.create({
      data: {
        ...createUser,
      },
    });
  }

  async findAll() {
    return this.database.seller.findMany();
  }

  async findOne(email: string) {
    return this.database.seller.findUnique({ where: { email } });
  }

  async update(id: number, updateSeller: Prisma.SellerUpdateInput) {
    return this.database.seller.update({ where: { seller_id: id }, data: updateSeller });
  }

  async remove(id: number) {
    return this.database.seller.delete({ where: { seller_id: id } });
  }
}
