"use client";

import { Heart, ShoppingCart, Store } from "lucide-react";
import Link from "next/link";

export function Navbar() {
  return (
    <header className="flex h-16 w-full items-center justify-between border-b bg-background px-4">
      <div className="flex items-center gap-4">
        <Link href="/" className="flex items-center gap-2 font-bold text-xl">
          <Store /> <span>E-Store</span>
        </Link>
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-accent rounded-full ">
          <Heart />
        </button>
        <Link href="/cart"  className="p-2 hover:bg-accent rounded-full ">
          <ShoppingCart />
      </Link>
      </div>
    </header>
  );
}
