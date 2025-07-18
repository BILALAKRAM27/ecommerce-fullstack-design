import { Controller, Get, Post, Body, Res, HttpStatus, HttpException, Req, UseGuards } from '@nestjs/common';
import { Response, Request } from 'express';
import { AuthService } from './auth.service';
import { JwtAuthGuard } from './jwt-auth.guard';
import { Prisma } from 'generated/prisma';
import * as bcrypt from 'bcrypt';
import { SellerService } from 'src/seller/seller.service';
import { BuyerService } from 'src/buyer/buyer.service';

// Define the user object structure from JWT
interface JwtUser {
  userId: number;
  email: string;
}

@Controller('seller_auth')
export class AuthController {
    constructor(
        private readonly authService: AuthService,
        private readonly sellerService: SellerService,
        private readonly buyerService: BuyerService
    ) {}

    @Get('login')
    getLogin(@Res() res: Response) {
      return res.render('seller_auth/login', { title: 'Login' });
    }

    @Get('register')
    getRegister(@Res() res: Response) {
      return res.render('seller_auth/register', { title: 'Register Here' });
    }

    @Post('login')
    async login(
      @Body() loginData: { email: string; password: string; userType: 'seller' | 'buyer' },
      @Res() res: Response
    ) {
      try {
        // Validate user credentials based on userType
        const user = await this.authService.validateUser(
          loginData.email,
          loginData.password,
          loginData.userType
        );
        if (!user) {
          throw new HttpException('Invalid email or password', HttpStatus.UNAUTHORIZED);
        }
        // Generate JWT token
        const result = await this.authService.login(user);
        // Redirect or respond based on userType
        return res.status(HttpStatus.OK).json({
          message: 'Login successful',
          access_token: result.access_token,
          userType: loginData.userType,
          user,
        });
      } catch (error) {
        if (error instanceof HttpException) throw error;
        throw new HttpException('Login failed', HttpStatus.INTERNAL_SERVER_ERROR);
      }
    }

    @Post('register')
    async register(
      @Body() registerData: {
        name: string;
        email: string;
        phone?: string;
        shop_name?: string;
        password: string;
        userType: 'seller' | 'buyer';
      },
      @Res() res: Response
    ) {
      try {
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(registerData.password, saltRounds);

        if (registerData.userType === 'seller') {
          // Check if seller already exists
          const existingSeller = await this.sellerService.findOne(registerData.email);
          if (existingSeller) {
            throw new HttpException('Seller with this email already exists', HttpStatus.CONFLICT);
          }
          const sellerData: Prisma.SellerCreateInput = {
            name: registerData.name,
            email: registerData.email,
            phone: registerData.phone || null,
            shop_name: registerData.shop_name || '',
            password_hash: hashedPassword,
            status: 'active'
          };
          const newSeller = await this.sellerService.create(sellerData);
          const { password_hash, ...userResponse } = newSeller;
          return res.status(HttpStatus.CREATED).json({
            message: 'Seller registered successfully',
            userType: 'seller',
            user: userResponse
          });
        } else if (registerData.userType === 'buyer') {
          // Check if buyer already exists
          const existingBuyer = await this.buyerService.findByEmail(registerData.email);
          if (existingBuyer) {
            throw new HttpException('Buyer with this email already exists', HttpStatus.CONFLICT);
          }
          const buyerData: Prisma.BuyerCreateInput = {
            name: registerData.name,
            email: registerData.email,
            phone: registerData.phone || null,
            password_hash: hashedPassword,
            status: 'active'
          };
          const newBuyer = await this.buyerService.create(buyerData);
          const { password_hash, ...userResponse } = newBuyer;
          return res.status(HttpStatus.CREATED).json({
            message: 'Buyer registered successfully',
            userType: 'buyer',
            user: userResponse
          });
        } else {
          throw new HttpException('Invalid user type', HttpStatus.BAD_REQUEST);
        }
      } catch (error) {
        if (error instanceof HttpException) {
          throw error;
        }
        throw new HttpException('Registration failed', HttpStatus.INTERNAL_SERVER_ERROR);
      }
    }

    @Post('logout')
    async logout(@Res() res: Response) {
      return res.status(HttpStatus.OK).json({
        message: 'Logout successful'
      });
    }

    @UseGuards(JwtAuthGuard)
    @Get('profile')
    async getProfile(
      @Req() req: Request & { user: JwtUser },
      @Res() res: Response
    ) {
      const userType = req.query.userType as 'seller' | 'buyer';
      const userEmail = req.user.email;
      if (userType === 'buyer') {
        const user = await this.buyerService.findByEmail(userEmail);
        if (!user) {
          throw new HttpException('User not found', HttpStatus.NOT_FOUND);
        }
        return res.json({
          buyer_id: user.buyer_id,
          email: user.email,
          name: user.name,
          phone: user.phone
        });
      } else {
        const user = await this.sellerService.findOne(userEmail);
        if (!user) {
          throw new HttpException('User not found', HttpStatus.NOT_FOUND);
        }
        return res.json({
          seller_id: user.seller_id,
          email: user.email,
          name: user.name,
          shop_name: user.shop_name,
          phone: user.phone
        });
      }
    }

    @Get('profile_page')
    getProfilePage(@Res() res: Response, @Req() req: Request) {
      const userType = req.query.userType as 'seller' | 'buyer';
      if (userType === 'buyer') {
        return res.render('buyer_auth/profile_page', { title: 'Profile' });
      } else {
        return res.render('seller_auth/profile_page', { title: 'Profile' });
      }
    }    }

