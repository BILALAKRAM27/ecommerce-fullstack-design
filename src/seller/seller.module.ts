import { Module } from '@nestjs/common';
import { SellerService } from './seller.service';
import { SellerController } from './seller.controller';
import { DatabaseModule } from 'src/database/database.module';

@Module({
  controllers: [SellerController],
  providers: [SellerService],
  imports: [DatabaseModule],
  exports: [SellerService],
})
export class SellerModule {}
