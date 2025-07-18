import { Injectable } from '@nestjs/common';
import { Prisma } from 'generated/prisma';
import { DatabaseService } from 'src/database/database.service';
import * as bcrypt from 'bcrypt';

@Injectable()
export class BuyerService {
  constructor(private database: DatabaseService) {}
  async findByEmail(email: string) {
    return this.database.buyer.findUnique({
      where: { email },
    });
  }

  async create(createUser: Prisma.BuyerCreateInput) {
      const saltRounds = 10;
      const hashedPassword = await bcrypt.hash(createUser.password_hash, saltRounds);

      // Replace the plain password with the hashed one
      return this.database.buyer.create({
        data: {
          ...createUser,
          password_hash: hashedPassword, // or whatever your field is called
        },
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
