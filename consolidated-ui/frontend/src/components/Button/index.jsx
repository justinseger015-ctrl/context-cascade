"use client";
import Link from "next/link";
import React, {forwardRef} from "react";
import css from "./index.module.scss";
import LoadingSvg from "/public/icons/loading.svg";
import tag from "@/utils/tag";

function Inner({icon, children}){
  return <>
    <span className={css.text}>{icon || children}</span>
    <span className={css.spinner}>
      <LoadingSvg/>
    </span>
  </>;
}


/**
 * a flexible button component that can render as either a `<Link>` or a `<button>`,
 * depending on whether an `href` is provided.
 *
 * @param {object} props - The component props.
 * @param {boolean} ghost - If true, applies ghost button styling.
 * @param {boolean} grayscale - If true, applies all-white or all-black styling (based on `dark`).
 * @param {string} href- The URL that the button links to. Renders as a `<button>` if not provided.
 * @param {function} onClick - The click event handler.
 * @param {React.ReactNode} children - The content of the button.
 * @param {string} className - Additional custom class names for the button.
 * @param {React.ReactNode} icon - SVG icon. If present, the button will displace as a circle with the icon.
 * @param {boolean} disabled - If true, disables the button.
 * @param {boolean} transparent - If true, applies transparent background styling.
 * @param {boolean} loading - If true, shows a loading indicator.
 * @param {boolean} wrap - If true, allows text wrapping inside the button.
 * @param {string} target - The target attribute for the link. Default is `_self`.
 * @param {boolean} prefetch - Prefetch the page for the link. Only applies when `href` is provided.
 * @param {React.Ref} ref - Ref forwarding for the component.
 * @returns {React.ReactElement} A button or a link element styled according to the provided props.
 */
export default forwardRef(({
  ghost = false,
  grayscale = false,
  href = "",
  onClick = null,
  children,
  className = "",
  icon = null,
  disabled = false,
  transparent = false,
  loading = false,
  wrap = false,
  target = "_self",
  prefetch = true,
  helperText = null,
}, ref) => {
  let thisClassName = `custom ${className} ${css.button}`;
  thisClassName += ` ${ghost ? css.ghost : ""}`;
  thisClassName += ` ${grayscale ? css.grayscale : ""}`;
  thisClassName += ` ${icon ? css.icon : ""}`;
  thisClassName += ` ${disabled ? css.disabled : ""}`;
  thisClassName += ` ${transparent ? css.transparent : ""}`;
  thisClassName += ` ${loading ? css.loading : ""}`;
  thisClassName += ` ${wrap ? css.wrap : ""}`;

  //log click event and call onClick handler
  function handleClick(e){
    tag("buttonClick", {
      text: children?.toString() || "iconbutton",
      ghost,
      grayscale,
      className,
      disabled,
      transparent,
      loading,
      wrap,
      target,
    });

    if (onClick){
      onClick(e);
    }
  }



  if (href){
    return <Link
      href={href}
      className={thisClassName}
      onClick={handleClick}
      target={target}
      prefetch={prefetch}
      ref={ref}
    >
      <Inner icon={icon}>{children}</Inner>
      {helperText && <div className={css.helperText}>{helperText}</div>}
    </Link>;
  }
  return <button
    className={thisClassName}
    onClick={handleClick}
    ref={ref}
  >
    <Inner icon={icon}>{children}</Inner>
    {helperText && <div className={css.helperText}>{helperText}</div>}
  </button>;
});
