import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DatabaseModule } from './database/database.module';
import { AuthModule } from './auth/auth.module';
import { SellerModule } from './seller/seller.module';
import { BuyerModule } from './buyer/buyer.module';


@Module({
  imports: [DatabaseModule, AuthModule, SellerModule, BuyerModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
