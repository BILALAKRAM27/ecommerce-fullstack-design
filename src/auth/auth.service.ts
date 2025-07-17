
import { Injectable } from '@nestjs/common';
import { SellerService } from 'src/seller/seller.service';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';

@Injectable()
export class AuthService {
  constructor(
    private sellerService: SellerService,
    private jwtService: JwtService
  ) {}

  async validateUser(email: string, password: string): Promise<any> {
    const user = await this.sellerService.findOne(email);
    if (user && await bcrypt.compare(password, user.password_hash)) {
      const { password_hash, ...result } = user;
      return result;
    }
    return null;
  }

  async login(user: any) {
    const payload = { email: user.email, sub: user.user_id };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }
}
