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
    console.log('Starting user validation:', { email, userType });
    
    let user;
    try {
      if (userType === 'seller') {
        user = await this.sellerService.findOne(email);
        console.log('Seller lookup result:', { 
          found: !!user,
          email,
          hasPasswordHash: user?.password_hash ? 'yes' : 'no'
        });
      } else if (userType === 'buyer') {
        user = await this.buyerService.findByEmail(email);
        console.log('Buyer lookup result:', { 
          found: !!user,
          email,
          hasPasswordHash: user?.password_hash ? 'yes' : 'no'
        });
      } else {
        console.log('Invalid user type:', userType);
        return null;
      }

      if (!user) {
        console.log('User not found:', { email, userType });
        return null;
      }

      console.log('Attempting password comparison for:', { email, userType });
      const passwordMatch = await bcrypt.compare(password, user.password_hash);
      console.log('Password validation result:', {
        email,
        userType,
        passwordMatch
      });
      
      if (passwordMatch) {
        const { password_hash, ...result } = user;
        return result;
      }

      console.log('Password did not match for:', { email, userType });
      return null;
    } catch (error) {
      console.error('Error during user validation:', { email, userType, error: error.message });
      return null;
    }
  }

  async login(user: any) {
    const payload = { email: user.email, sub: user.user_id };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }
}
