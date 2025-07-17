import { Module } from '@nestjs/common';
import { AuthService } from './auth.service';
import { JwtModule } from '@nestjs/jwt';
import { jwtConstants } from './constants';
import { LocalStrategy } from './local.strategy';   
import { JwtStrategy } from './jwt.strategy';
import { PassportModule } from '@nestjs/passport';
import { AuthController } from './auth.controller';
import { SellerModule } from 'src/seller/seller.module';
@Module({
  imports: [SellerModule, JwtModule.register({
    secret: jwtConstants.secret,
    signOptions: { expiresIn: '1 hour' },
  }), PassportModule],
  providers: [AuthService, LocalStrategy, JwtStrategy],
  exports: [AuthService],
  controllers: [AuthController],
})
export class AuthModule {}
