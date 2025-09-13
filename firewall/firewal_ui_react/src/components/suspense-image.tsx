import { useState, useEffect } from "react";
import { Skeleton } from "./ui/skeleton";

type SuspenseImageProps = {
    src: string
} & React.ImgHTMLAttributes<HTMLImageElement>

export function SuspenseImage({ src, ...props }: SuspenseImageProps) {
    const [isLoaded, setIsLoaded] = useState(false);
    const [error, setError] = useState(false);

    useEffect(() => {
        const img = new Image();
        img.src = src;
        img.onload = () => setIsLoaded(true);
        img.onerror = () => setError(true);
    }, [src]);

    if (error) return <div>Failed to load image</div>;
    if (!isLoaded) return <Skeleton className={props.className} />;

    return <img src={src} {...props} />;
}
