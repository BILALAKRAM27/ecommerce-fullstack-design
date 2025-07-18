import { Injectable } from '@nestjs/common';
import { SellerService } from 'src/seller/seller.service';
import { BuyerService } from 'src/buyer/buyer.service'; // <-- Import BuyerService
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';

@Injectable()
export class AuthService {
  constructor(
    private sellerService: SellerService,
    private buyerService: BuyerService, // <-- Inject BuyerService
    private jwtService: JwtService
  ) {}

  async validateUser(email: string, password: string, userType: 'seller' | 'buyer'): Promise<any> {
    let user;
    if (userType === 'seller') {
      user = await this.sellerService.findOne(email);
    } else if (userType === 'buyer') {
      user = await this.buyerService.findByEmail(email);
    } else {
      return null;
    }
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
