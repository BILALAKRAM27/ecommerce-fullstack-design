import { Injectable } from '@nestjs/common';
import { Prisma } from 'generated/prisma';
import { DatabaseService } from 'src/database/database.service';

@Injectable()
export class BuyerService {
  constructor(private database: DatabaseService) {}
  async findByEmail(email: string) {
    return this.database.buyer.findUnique({
      where: { email },
    });
  }
  async create(createBuyer: Prisma.BuyerCreateInput) {
    return this.database.buyer.create({
      data: createBuyer,
    });
  }

  async findAll() {
    return this.database.buyer.findMany();
  }

  async findOne(id: number) {
    return this.database.buyer.findUnique({
      where: { buyer_id: id },
    });
  }

  async update(id: number, updateBuyer: Prisma.BuyerUpdateInput) {
    return this.database.buyer.update({
      where: { buyer_id: id },
      data: updateBuyer,
    });
  }

  async remove(id: number) {
    return this.database.buyer.delete({
      where: { buyer_id: id },
    });
  }
}
