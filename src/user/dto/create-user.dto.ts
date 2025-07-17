import { IsEmail, IsString, IsOptional, IsEnum, MinLength, IsPhoneNumber } from 'class-validator';

export class CreateUserDto {
  @IsString()
  name: string;

  @IsEmail()
  email: string;

  @IsOptional()
  @IsPhoneNumber()
  phone?: string;

  @IsEnum(['buyer', 'seller', 'admin'])
  role: 'buyer' | 'seller' | 'admin';

  @IsString()
  @MinLength(8)
  password: string;
}
