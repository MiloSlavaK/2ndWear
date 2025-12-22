import { Send } from "lucide-react";

interface ProductCardProps {
  product: {
    id: string;
    title: string;
    price: number;
    size?: string;
    color?: string;
    style?: string;
    image_url?: string;
    seller_username?: string;
    seller_contact?: string;
  };
}

export function ProductCard({ product }: ProductCardProps) {
  const displayContact = product.seller_username
    ? `@${product.seller_username}`
    : product.seller_contact || "Нет контакта";
  const imageSrc = product.image_url || "https://via.placeholder.com/400x500?text=No+Image";
  const orderIdShort = product.id ? product.id.slice(0, 6) : "----";
  const contactHref = product.seller_username
    ? `https://t.me/${product.seller_username}`
    : product.seller_contact
      ? (product.seller_contact.startsWith("+") || /\d/.test(product.seller_contact) ? `tel:${product.seller_contact}` : undefined)
      : undefined;
  return (
    <div className="bg-card rounded-lg overflow-hidden border border-border hover:shadow-lg transition-shadow duration-300">
      <div className="aspect-[3/4] overflow-hidden">
        <img
          src={imageSrc}
          alt={product.title}
          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
        />
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="flex-1">{product.title}</h3>
          <span className="text-xs text-muted-foreground ml-2">#{orderIdShort}</span>
        </div>
        <div className="flex items-center justify-between mb-2">
          <p className="text-muted-foreground">Размер: {product.size || "-"}</p>
          <p className="text-primary">{product.price} ₽</p>
        </div>
        <div className="flex gap-2 mb-3">
          <span className="px-2 py-1 bg-secondary text-secondary-foreground rounded text-sm">
            {product.style || "Стиль"}
          </span>
          <span className="px-2 py-1 bg-accent text-accent-foreground rounded text-sm">
            {product.color || "Цвет"}
          </span>
        </div>
        {contactHref ? (
          <a
            href={contactHref}
            target="_blank"
            rel="noopener noreferrer"
            className="w-full bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:opacity-90 transition-opacity flex items-center justify-between"
          >
            <div className="flex items-center gap-2">
              <Send className="w-4 h-4" />
              <span>Связаться</span>
            </div>
            <span className="text-sm">{displayContact}</span>
          </a>
        ) : (
          <div className="w-full bg-primary text-primary-foreground px-4 py-2 rounded-lg flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Send className="w-4 h-4" />
              <span>Связаться</span>
            </div>
            <span className="text-sm">{displayContact}</span>
          </div>
        )}
      </div>
    </div>
  );
}