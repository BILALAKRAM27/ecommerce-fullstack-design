import { Injectable } from '@nestjs/common';
import { Prisma,User } from 'generated/prisma';
import { DatabaseService } from 'src/database/database.service';
import * as bcrypt from 'bcrypt';

@Injectable()
export class UserService {
  constructor(private readonly databaseService: DatabaseService) {}
  async create(createUser: Prisma.UserCreateInput) {
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(createUser.password_hash, saltRounds);

    // Replace the plain password with the hashed one
    return this.databaseService.user.create({
      data: {
        ...createUser,
        password_hash: hashedPassword, // or whatever your field is called
      },
    });
  }

  async findAll(Role?: 'seller' | 'buyer' | 'admin', Status?: 'active' | 'suspended' | 'banned') {
    if (Role && Status) {
      return this.databaseService.user.findMany({
        where: {
          role: Role,
          status: Status,
        },
      });
    } else if (Role) {
      return this.databaseService.user.findMany({
        where: {
          role: Role,
        },
      });
    } else if (Status) {
      return this.databaseService.user.findMany({
        where: {
          status: Status,
        },
      });
    } else {
      return this.databaseService.user.findMany();
    }
  }
  

  async findOne(email: string): Promise<User | undefined> {
    const result = await this.databaseService.user.findUnique({where:{email:email}});
    return result === null ? undefined : result;
  }

  async update(id: number, updateUser: Prisma.UserUpdateInput) {
    return this.databaseService.user.update({
      where: {user_id: id},
      data: updateUser,
    });
  }

  async remove(id: number) {
    return this.databaseService.user.delete({
      where: {user_id: id},
    });
  }
} 
