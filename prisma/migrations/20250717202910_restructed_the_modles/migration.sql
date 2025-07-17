/*
  Warnings:

  - You are about to drop the column `user_id` on the `Admin` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `Cart` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `Order` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `ProductReview` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `Seller` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `Wishlist` table. All the data in the column will be lost.
  - You are about to drop the `User` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[email]` on the table `Admin` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[buyer_id]` on the table `Cart` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[email]` on the table `Seller` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `email` to the `Admin` table without a default value. This is not possible if the table is not empty.
  - Added the required column `name` to the `Admin` table without a default value. This is not possible if the table is not empty.
  - Added the required column `password_hash` to the `Admin` table without a default value. This is not possible if the table is not empty.
  - Added the required column `buyer_id` to the `Cart` table without a default value. This is not possible if the table is not empty.
  - Added the required column `buyer_id` to the `Order` table without a default value. This is not possible if the table is not empty.
  - Added the required column `buyer_id` to the `ProductReview` table without a default value. This is not possible if the table is not empty.
  - Added the required column `email` to the `Seller` table without a default value. This is not possible if the table is not empty.
  - Added the required column `name` to the `Seller` table without a default value. This is not possible if the table is not empty.
  - Added the required column `password_hash` to the `Seller` table without a default value. This is not possible if the table is not empty.
  - Added the required column `buyer_id` to the `Wishlist` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "Admin" DROP CONSTRAINT "Admin_user_id_fkey";

-- DropForeignKey
ALTER TABLE "Cart" DROP CONSTRAINT "Cart_user_id_fkey";

-- DropForeignKey
ALTER TABLE "Order" DROP CONSTRAINT "Order_user_id_fkey";

-- DropForeignKey
ALTER TABLE "ProductReview" DROP CONSTRAINT "ProductReview_user_id_fkey";

-- DropForeignKey
ALTER TABLE "Seller" DROP CONSTRAINT "Seller_user_id_fkey";

-- DropForeignKey
ALTER TABLE "Wishlist" DROP CONSTRAINT "Wishlist_user_id_fkey";

-- DropIndex
DROP INDEX "Admin_user_id_key";

-- DropIndex
DROP INDEX "Cart_user_id_key";

-- DropIndex
DROP INDEX "Seller_user_id_key";

-- AlterTable
ALTER TABLE "Admin" DROP COLUMN "user_id",
ADD COLUMN     "email" TEXT NOT NULL,
ADD COLUMN     "name" TEXT NOT NULL,
ADD COLUMN     "password_hash" TEXT NOT NULL,
ADD COLUMN     "phone" TEXT,
ADD COLUMN     "status" "UserStatus" NOT NULL DEFAULT 'active';

-- AlterTable
ALTER TABLE "Cart" DROP COLUMN "user_id",
ADD COLUMN     "buyer_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "Order" DROP COLUMN "user_id",
ADD COLUMN     "buyer_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "ProductReview" DROP COLUMN "user_id",
ADD COLUMN     "buyer_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "Seller" DROP COLUMN "user_id",
ADD COLUMN     "email" TEXT NOT NULL,
ADD COLUMN     "name" TEXT NOT NULL,
ADD COLUMN     "password_hash" TEXT NOT NULL,
ADD COLUMN     "phone" TEXT,
ADD COLUMN     "status" "UserStatus" NOT NULL DEFAULT 'active';

-- AlterTable
ALTER TABLE "Wishlist" DROP COLUMN "user_id",
ADD COLUMN     "buyer_id" INTEGER NOT NULL;

-- DropTable
DROP TABLE "User";

-- DropEnum
DROP TYPE "Role";

-- CreateTable
CREATE TABLE "Buyer" (
    "buyer_id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password_hash" TEXT NOT NULL,
    "phone" TEXT,
    "status" "UserStatus" NOT NULL DEFAULT 'active',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Buyer_pkey" PRIMARY KEY ("buyer_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Buyer_email_key" ON "Buyer"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Admin_email_key" ON "Admin"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Cart_buyer_id_key" ON "Cart"("buyer_id");

-- CreateIndex
CREATE UNIQUE INDEX "Seller_email_key" ON "Seller"("email");

-- AddForeignKey
ALTER TABLE "ProductReview" ADD CONSTRAINT "ProductReview_buyer_id_fkey" FOREIGN KEY ("buyer_id") REFERENCES "Buyer"("buyer_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Cart" ADD CONSTRAINT "Cart_buyer_id_fkey" FOREIGN KEY ("buyer_id") REFERENCES "Buyer"("buyer_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Wishlist" ADD CONSTRAINT "Wishlist_buyer_id_fkey" FOREIGN KEY ("buyer_id") REFERENCES "Buyer"("buyer_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Order" ADD CONSTRAINT "Order_buyer_id_fkey" FOREIGN KEY ("buyer_id") REFERENCES "Buyer"("buyer_id") ON DELETE RESTRICT ON UPDATE CASCADE;
