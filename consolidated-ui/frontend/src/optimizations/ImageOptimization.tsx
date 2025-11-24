/**
 * Image Optimization Utilities
 *
 * Features:
 * - WebP format with fallback
 * - Lazy loading with Intersection Observer
 * - Responsive images (srcset, sizes)
 * - Progressive loading (blur placeholder)
 *
 * P4_T8: Frontend Optimization - Image Performance
 * Target: Improve LCP (Largest Contentful Paint)
 */

import React, { useState, useEffect, useRef, ImgHTMLAttributes } from 'react';

interface OptimizedImageProps extends ImgHTMLAttributes<HTMLImageElement> {
  src: string;
  alt: string;
  webpSrc?: string;
  srcSet?: string;
  sizes?: string;
  priority?: boolean; // If true, skip lazy loading (for LCP images)
  blurDataURL?: string; // Placeholder for progressive loading
  onLoad?: () => void;
}

/**
 * Optimized Image Component
 *
 * - Uses WebP with fallback to original format
 * - Lazy loads images using Intersection Observer
 * - Supports responsive images (srcset, sizes)
 * - Progressive loading with blur placeholder
 */
export const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  webpSrc,
  srcSet,
  sizes,
  priority = false,
  blurDataURL,
  onLoad,
  className = '',
  ...rest
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(priority); // Priority images load immediately
  const imgRef = useRef<HTMLImageElement>(null);

  // Intersection Observer for lazy loading
  useEffect(() => {
    if (priority) return; // Skip lazy loading for priority images

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      {
        rootMargin: '100px', // Start loading 100px before visible
      }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => {
      if (imgRef.current) {
        observer.unobserve(imgRef.current);
      }
    };
  }, [priority]);

  const handleLoad = () => {
    setIsLoaded(true);
    onLoad?.();
  };

  return (
    <picture>
      {/* WebP source (modern browsers) */}
      {webpSrc && isInView && (
        <source type="image/webp" srcSet={webpSrc} sizes={sizes} />
      )}

      {/* Original format fallback */}
      <img
        ref={imgRef}
        src={isInView ? src : blurDataURL || 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='}
        srcSet={isInView ? srcSet : undefined}
        sizes={sizes}
        alt={alt}
        loading={priority ? 'eager' : 'lazy'}
        decoding="async"
        onLoad={handleLoad}
        className={`${className} ${!isLoaded && blurDataURL ? 'blur-placeholder' : ''}`}
        {...rest}
      />
    </picture>
  );
};

/**
 * Generate responsive image srcSet
 *
 * Example:
 * const srcSet = generateSrcSet('/images/hero.jpg', [400, 800, 1200]);
 * // Returns: "/images/hero-400.jpg 400w, /images/hero-800.jpg 800w, /images/hero-1200.jpg 1200w"
 */
export function generateSrcSet(
  baseUrl: string,
  widths: number[]
): string {
  return widths
    .map((width) => {
      const url = baseUrl.replace(/\.(jpg|jpeg|png|webp)$/, `-${width}.$1`);
      return `${url} ${width}w`;
    })
    .join(', ');
}

/**
 * Image format converter utility
 *
 * Converts image URLs to WebP format
 * Assumes a CDN or image optimization service that supports WebP conversion
 */
export function toWebP(url: string): string {
  // If using a CDN with WebP support (e.g., Cloudinary, Imgix)
  // Replace with your CDN's WebP conversion pattern
  return url.replace(/\.(jpg|jpeg|png)$/, '.webp');
}

/**
 * Generate blur placeholder data URL
 *
 * Creates a tiny blurred version of the image for progressive loading
 * In production, generate these at build time using Sharp or similar
 */
export function generateBlurDataURL(width: number = 10, height: number = 10): string {
  // This is a simplified example
  // In production, use a library like plaiceholder or sharp
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;

  const ctx = canvas.getContext('2d');
  if (!ctx) return '';

  // Create gradient placeholder
  const gradient = ctx.createLinearGradient(0, 0, width, height);
  gradient.addColorStop(0, '#e0e0e0');
  gradient.addColorStop(1, '#f0f0f0');

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);

  return canvas.toDataURL();
}

/**
 * Preload critical images for LCP optimization
 *
 * Call this in your app's head for hero images or above-the-fold content
 */
export function preloadImage(src: string, as: 'image' = 'image') {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.as = as;
  link.href = src;
  document.head.appendChild(link);
}

/**
 * Example usage:
 *
 * // Hero image (priority, no lazy loading)
 * <OptimizedImage
 *   src="/images/hero.jpg"
 *   webpSrc="/images/hero.webp"
 *   srcSet={generateSrcSet('/images/hero.jpg', [400, 800, 1200])}
 *   sizes="(max-width: 768px) 100vw, 50vw"
 *   alt="Hero image"
 *   priority={true}
 *   blurDataURL="/images/hero-blur.jpg"
 * />
 *
 * // Below-the-fold image (lazy loaded)
 * <OptimizedImage
 *   src="/images/thumbnail.jpg"
 *   webpSrc="/images/thumbnail.webp"
 *   alt="Thumbnail"
 *   blurDataURL={generateBlurDataURL(10, 10)}
 * />
 */

/**
 * CSS for blur placeholder effect
 *
 * Add to your global CSS or Tailwind config:
 *
 * .blur-placeholder {
 *   filter: blur(10px);
 *   transition: filter 0.3s ease-in-out;
 * }
 *
 * .blur-placeholder.loaded {
 *   filter: blur(0);
 * }
 */
