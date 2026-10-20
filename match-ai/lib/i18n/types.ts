import type { en } from "./messages/en";

/** Recursively widens literal string types so other locales can have different text. */
export type DeepWiden<T> = T extends string
  ? string
  : T extends readonly (infer U)[]
    ? readonly DeepWiden<U>[]
    : T extends object
      ? { readonly [K in keyof T]: DeepWiden<T[K]> }
      : T;

/** Shape every locale dictionary must satisfy. */
export type Messages = DeepWiden<typeof en>;

/** Dot-separated paths to string leaves (arrays are not traversed). */
export type MessageKey<T = Messages, Prefix extends string = ""> = {
  [K in keyof T & string]: T[K] extends string
    ? `${Prefix}${K}`
    : T[K] extends readonly unknown[]
      ? never
      : T[K] extends object
        ? MessageKey<T[K], `${Prefix}${K}.`>
        : never;
}[keyof T & string];

export type MessageVars = Record<string, string | number>;
