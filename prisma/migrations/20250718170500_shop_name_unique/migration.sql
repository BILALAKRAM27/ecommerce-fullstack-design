/*
  Warnings:

  - A unique constraint covering the columns `[shop_name]` on the table `Seller` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Seller_shop_name_key" ON "Seller"("shop_name");
