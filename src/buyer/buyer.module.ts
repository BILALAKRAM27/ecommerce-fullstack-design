import { Module } from '@nestjs/common';
import { BuyerService } from './buyer.service';
import { BuyerController } from './buyer.controller';
import { DatabaseService } from 'src/database/database.service';
import { DatabaseModule } from 'src/database/database.module';

@Module({
  controllers: [BuyerController],
  providers: [BuyerService],
  imports: [DatabaseModule],
  exports: [BuyerService],
})
export class BuyerModule {}
