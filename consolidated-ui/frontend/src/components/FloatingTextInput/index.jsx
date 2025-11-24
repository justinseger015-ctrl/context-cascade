"use client";
import React, { useState, useRef, forwardRef, useImperativeHandle } from "react";
import css from "./index.module.scss";

/**
 * a floating label text input component with validation and multiline support.
 * @param {string} [name=""] - The name attribute of the input element.
 * @param {Array} [validators=[]] - An array of validator functions to validate the input value.
 * @param {Function} [onfocus=() => {}] - Callback function triggered when the input is focused.
 * @param {Function} [onBlur=() => {}] - Callback function triggered when the input loses focus.
 * @param {Function} [onChange=() => {}] - Callback function triggered when the input value changes.
 * @param {Function} [onFinish=() => {}] - Callback function triggered when the user finishes typing (a short delay after the last input change).
 * @param {Function} [onEnter=() => {}] - Callback function triggered when the Enter key is pressed.
 * @param {string} [type="text"] - The type attribute of the input element.
 * @param {string} [autocomplete="off"] - The autocomplete attribute of the input element.
 * @param {string} [label=""] - The label text for the input.
 * @param {boolean} [multiline=false] - If true, renders a textarea instead of an input.
 * @param {string} [initialValue=""] - The initial value of the input.
 * @param {string} [className=""] - Additional CSS class name for the component.
 * @param {boolean} [disabled=false] - If true, disables the input.
 * @param {string} [helperText=""] - The helper text to display below the input.
 * @param {string} [prefixText=""] - The prefix text to display inside the input.
 */
const FloatingTextInput = forwardRef(({
  name = "",
  validators = [],
  onfocus = () => {},
  onBlur = () => {},
  onChange = () => {},
  onFinish = () => {},
  onEnter = () => {},
  type = "text",
  autocomplete = "off",
  label = "",
  multiline = false,
  initialValue = "",
  className = "",
  disabled = false,
  helperText = "",
  prefixText = "",
}, ref) => {
  const [message, setMessage] = useState(helperText);
  const [value, setValue] = useState(initialValue);
  const [validity, setValidity] = useState(null);
  const [finished, setFinished] = useState(null);
  const inputRef = useRef();

  let fullClassName = `${css.floatingTextInput} ${className}`;
  fullClassName += `${multiline ? css.multiline : ""}`;
  fullClassName += `${disabled ? css.disabled : ""}`;
  fullClassName += `${validity === true ? css.valid : ""}`;
  fullClassName += `${validity === false ? css.invalid : ""}`;

  const validate = async(newValue) => {
    for (const validator of validators) {
      if (await validator.test(newValue)) {
        setMessage(validator.message || helperText);
        setValidity(validator.valid);
        return validator.valid;
      }
    }
    return true;
  };

  useImperativeHandle(ref, () => ({
    isValid: () => validate(value),
    getValue: () => value,
    setValid: (newValidity) => setValidity(newValidity),
    setMessage: (newMessage) => setMessage(newMessage),
    setValue: (newValue) => {
      setValue(newValue);
      if (multiline) {
        inputRef.current.value = newValue;
        inputRef.current.style.height = "0px";
        inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
      }
      return newValue;
    },
  }));

  const handleChange = (event) => {
    const newValue = event.target.value;
    setValue(newValue);
    onChange(newValue);

    clearTimeout(finished);
    setFinished(setTimeout(() => {
      const isValid = validate(newValue);
      onFinish(newValue, isValid);
    }, 300));
  };

  const handleBlur = (event) => {
    const isValid = validate(event.target.value);
    onBlur(event.target.value, isValid);
  };

  const handleKeyUp = (event) => {
    if (event.keyCode === 13) {
      clearTimeout(finished);
      onFinish(event.target.value);
      onEnter(event.target.value);
      if (!multiline) {
        event.target.blur();
      }
    }
  };

  return (
    <div className={fullClassName}>
      <div className={css.inputHolder}>
        {multiline ? (
          <textarea
            ref={inputRef}
            type={type}
            placeholder="x"
            className={css.input}
            name={name}
            value={value}
            onChange={handleChange}
            onFocus={onfocus}
            onBlur={handleBlur}
            autoComplete={autocomplete}
            onInput={() => {
              inputRef.current.style.height = "0px";
              inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
            }}
            onKeyUp={handleKeyUp}
          />
        ) : (
          <input
            ref={inputRef}
            type={type}
            placeholder="x"
            className={css.input}
            name={name}
            value={value}
            disabled={disabled}
            onChange={handleChange}
            onFocus={onfocus}
            onBlur={handleBlur}
            autoComplete={autocomplete}
            onKeyUp={handleKeyUp}
          />
        )}
        <span className={css.prefixText}>{prefixText}</span>
        <label htmlFor={name}>
          <span>{label}</span>
        </label>
      </div>
      <div className={css.message}>{message}</div>
    </div>
  );
});

export default FloatingTextInput;
