import { Controller, Get, Post, Body, Res, HttpStatus, HttpException, Req, UseGuards } from '@nestjs/common';
import { Response, Request } from 'express';
import { AuthService } from './auth.service';
import { UserService } from '../user/user.service';
import { JwtAuthGuard } from './jwt-auth.guard';
import { Prisma } from 'generated/prisma';
import * as bcrypt from 'bcrypt';

// Define the user object structure from JWT
interface JwtUser {
  userId: number;
  email: string;
}

@Controller('auth')
export class AuthController {
    constructor(
        private readonly authService: AuthService,
        private readonly userService: UserService
    ) {}

    @Get('login')
    getLogin(@Res() res: Response) {
      return res.render('auth/login', { title: 'User Login' });
    }

    @Get('register')
    getRegister(@Res() res: Response) {
      return res.render('auth/register', { title: 'Register Here' });
    }

    @Post('login')
    async login(@Body() loginData: { email: string; password: string }, @Res() res: Response) {
        try {
            // Validate user credentials
            const user = await this.authService.validateUser(loginData.email, loginData.password);
            if (!user) {
                throw new HttpException('Invalid email or password', HttpStatus.UNAUTHORIZED);
            }
            // Generate JWT token
            const result = await this.authService.login(user);
            return res.status(HttpStatus.OK).json({
                message: 'Login successful',
                access_token: result.access_token,
                user: {
                    user_id: user.user_id,
                    email: user.email,
                    name: user.name,
                    role: user.role
                }
            });
        } catch (error) {
            if (error instanceof HttpException) {
                throw error;
            }
            throw new HttpException('Login failed', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Post('register')
    async register(@Body() registerData: {
        name: string;
        email: string;
        phone?: string;
        role: 'buyer' | 'seller';
        password: string;
    }, @Res() res: Response) {
        try {
            // Check if user already exists
            const existingUser = await this.userService.findOne(registerData.email);
            if (existingUser) {
                throw new HttpException('User with this email already exists', HttpStatus.CONFLICT);
            }
            // Hash the password
            const saltRounds = 10;
            const hashedPassword = await bcrypt.hash(registerData.password, saltRounds);
            // Create user data for Prisma
            const userData: Prisma.UserCreateInput = {
                name: registerData.name,
                email: registerData.email,
                phone: registerData.phone || null,
                role: registerData.role,
                password_hash: hashedPassword,
                status: 'active'
            };
            // Create the user using the user service
            const newUser = await this.userService.create(userData);
            // Remove password from response
            const { password_hash, ...userResponse } = newUser;
            return res.status(HttpStatus.CREATED).json({
                message: 'User registered successfully',
                user: userResponse
            });
        } catch (error) {
            if (error instanceof HttpException) {
                throw error;
            }
            throw new HttpException('Registration failed', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Post('logout')
    async logout(@Res() res: Response) {
        // For JWT-in-header, logout is handled client-side by removing the token
        return res.status(HttpStatus.OK).json({
            message: 'Logout successful'
        });
    }

    @UseGuards(JwtAuthGuard)
    @Get('profile')
    async getProfile(@Req() req: Request & { user: JwtUser }) {
        // Return user data as JSON for SPA usage
        const userEmail = req.user.email;
        const user = await this.userService.findOne(userEmail);
        if (!user) {
            throw new HttpException('User not found', HttpStatus.NOT_FOUND);
        }
        // You can add more user info here if needed
        return {
            user_id: user.user_id,
            email: user.email,
            name: user.name,
            role: user.role,
            phone: user.phone
        };
    }

    @Get('profile_page')
    getProfilePage(@Res() res: Response) {
      return res.render('auth/profile_page', { title: 'User Profile' });
    }
}
