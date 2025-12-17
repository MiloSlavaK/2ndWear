import { Send } from "lucide-react";

interface Product {
  id: number;
  name: string;
  price: number;
  size: string;
  color: string;
  style: string;
  image: string;
  telegramLink: string;
}

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="bg-card rounded-lg overflow-hidden border border-border hover:shadow-lg transition-shadow duration-300">
      <div className="aspect-[3/4] overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
        />
      </div>
      <div className="p-4">
        <h3 className="mb-1">{product.name}</h3>
        <div className="flex items-center justify-between mb-2">
          <p className="text-muted-foreground">Размер: {product.size}</p>
          <p className="text-primary">{product.price} ₽</p>
        </div>
        <div className="flex gap-2 mb-3">
          <span className="px-2 py-1 bg-secondary text-secondary-foreground rounded text-sm">
            {product.style}
          </span>
          <span className="px-2 py-1 bg-accent text-accent-foreground rounded text-sm">
            {product.color}
          </span>
        </div>
        <a
          href={product.telegramLink}
          target="_blank"
          rel="noopener noreferrer"
          className="w-full bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
        >
          <Send className="w-4 h-4" />
          Купить
        </a>
      </div>
    </div>
  );
}