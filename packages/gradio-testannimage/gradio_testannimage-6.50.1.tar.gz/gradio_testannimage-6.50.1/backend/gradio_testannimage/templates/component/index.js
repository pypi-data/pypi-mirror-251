const {
  SvelteComponent: Et,
  assign: Nt,
  create_slot: Pt,
  detach: Rt,
  element: Tt,
  get_all_dirty_from_scope: At,
  get_slot_changes: Bt,
  get_spread_update: It,
  init: jt,
  insert: Ot,
  safe_not_equal: Zt,
  set_dynamic_element_data: Oe,
  set_style: E,
  toggle_class: H,
  transition_in: pt,
  transition_out: yt,
  update_slot_base: Ut
} = window.__gradio__svelte__internal;
function Dt(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), o = Pt(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-1t38q2d"
    }
  ], f = {};
  for (let a = 0; a < s.length; a += 1)
    f = Nt(f, s[a]);
  return {
    c() {
      e = Tt(
        /*tag*/
        l[14]
      ), o && o.c(), Oe(
        /*tag*/
        l[14]
      )(e, f), H(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), H(
        e,
        "padded",
        /*padding*/
        l[6]
      ), H(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), H(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), E(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), E(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), E(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), E(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), E(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), E(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), E(e, "border-width", "var(--block-border-width)");
    },
    m(a, r) {
      Ot(a, e, r), o && o.m(e, null), n = !0;
    },
    p(a, r) {
      o && o.p && (!n || r & /*$$scope*/
      131072) && Ut(
        o,
        i,
        a,
        /*$$scope*/
        a[17],
        n ? Bt(
          i,
          /*$$scope*/
          a[17],
          r,
          null
        ) : At(
          /*$$scope*/
          a[17]
        ),
        null
      ), Oe(
        /*tag*/
        a[14]
      )(e, f = It(s, [
        (!n || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!n || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!n || r & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), H(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), H(
        e,
        "padded",
        /*padding*/
        a[6]
      ), H(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), H(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), r & /*height*/
      1 && E(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), r & /*width*/
      2 && E(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), r & /*variant*/
      16 && E(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), r & /*allow_overflow*/
      2048 && E(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && E(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), r & /*min_width*/
      8192 && E(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      n || (pt(o, a), n = !0);
    },
    o(a) {
      yt(o, a), n = !1;
    },
    d(a) {
      a && Rt(e), o && o.d(a);
    }
  };
}
function Xt(l) {
  let e, t = (
    /*tag*/
    l[14] && Dt(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (pt(t, n), e = !0);
    },
    o(n) {
      yt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Yt(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: s = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: r = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: m = "normal" } = e, { test_id: g = void 0 } = e, { explicit_call: c = !1 } = e, { container: y = !0 } = e, { visible: L = !0 } = e, { allow_overflow: S = !0 } = e, { scale: C = null } = e, { min_width: d = 0 } = e, v = m === "fieldset" ? "fieldset" : "div";
  const M = (w) => {
    if (w !== void 0) {
      if (typeof w == "number")
        return w + "px";
      if (typeof w == "string")
        return w;
    }
  };
  return l.$$set = (w) => {
    "height" in w && t(0, o = w.height), "width" in w && t(1, s = w.width), "elem_id" in w && t(2, f = w.elem_id), "elem_classes" in w && t(3, a = w.elem_classes), "variant" in w && t(4, r = w.variant), "border_mode" in w && t(5, _ = w.border_mode), "padding" in w && t(6, u = w.padding), "type" in w && t(16, m = w.type), "test_id" in w && t(7, g = w.test_id), "explicit_call" in w && t(8, c = w.explicit_call), "container" in w && t(9, y = w.container), "visible" in w && t(10, L = w.visible), "allow_overflow" in w && t(11, S = w.allow_overflow), "scale" in w && t(12, C = w.scale), "min_width" in w && t(13, d = w.min_width), "$$scope" in w && t(17, i = w.$$scope);
  }, [
    o,
    s,
    f,
    a,
    r,
    _,
    u,
    g,
    c,
    y,
    L,
    S,
    C,
    d,
    v,
    M,
    m,
    i,
    n
  ];
}
class Kt extends Et {
  constructor(e) {
    super(), jt(this, e, Yt, Xt, Zt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Wt,
  append: Ee,
  attr: pe,
  create_component: Gt,
  destroy_component: Ht,
  detach: Jt,
  element: Ze,
  init: Qt,
  insert: xt,
  mount_component: $t,
  safe_not_equal: el,
  set_data: tl,
  space: ll,
  text: nl,
  toggle_class: J,
  transition_in: il,
  transition_out: sl
} = window.__gradio__svelte__internal;
function ol(l) {
  let e, t, n, i, o, s;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = Ze("label"), t = Ze("span"), Gt(n.$$.fragment), i = ll(), o = nl(
        /*label*/
        l[0]
      ), pe(t, "class", "svelte-9gxdi0"), pe(e, "for", ""), pe(e, "data-testid", "block-label"), pe(e, "class", "svelte-9gxdi0"), J(e, "hide", !/*show_label*/
      l[2]), J(e, "sr-only", !/*show_label*/
      l[2]), J(
        e,
        "float",
        /*float*/
        l[4]
      ), J(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(f, a) {
      xt(f, e, a), Ee(e, t), $t(n, t, null), Ee(e, i), Ee(e, o), s = !0;
    },
    p(f, [a]) {
      (!s || a & /*label*/
      1) && tl(
        o,
        /*label*/
        f[0]
      ), (!s || a & /*show_label*/
      4) && J(e, "hide", !/*show_label*/
      f[2]), (!s || a & /*show_label*/
      4) && J(e, "sr-only", !/*show_label*/
      f[2]), (!s || a & /*float*/
      16) && J(
        e,
        "float",
        /*float*/
        f[4]
      ), (!s || a & /*disable*/
      8) && J(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      s || (il(n.$$.fragment, f), s = !0);
    },
    o(f) {
      sl(n.$$.fragment, f), s = !1;
    },
    d(f) {
      f && Jt(e), Ht(n);
    }
  };
}
function fl(l, e, t) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: s = !1 } = e, { float: f = !0 } = e;
  return l.$$set = (a) => {
    "label" in a && t(0, n = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, s = a.disable), "float" in a && t(4, f = a.float);
  }, [n, i, o, s, f];
}
class al extends Wt {
  constructor(e) {
    super(), Qt(this, e, fl, ol, el, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: rl,
  append: _l,
  attr: Ne,
  binding_callbacks: ul,
  create_slot: cl,
  detach: dl,
  element: Ue,
  get_all_dirty_from_scope: ml,
  get_slot_changes: bl,
  init: gl,
  insert: hl,
  safe_not_equal: wl,
  toggle_class: Q,
  transition_in: kl,
  transition_out: pl,
  update_slot_base: yl
} = window.__gradio__svelte__internal;
function vl(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[5].default
  ), o = cl(
    i,
    l,
    /*$$scope*/
    l[4],
    null
  );
  return {
    c() {
      e = Ue("div"), t = Ue("div"), o && o.c(), Ne(t, "class", "icon svelte-3w3rth"), Ne(e, "class", "empty svelte-3w3rth"), Ne(e, "aria-label", "Empty value"), Q(
        e,
        "small",
        /*size*/
        l[0] === "small"
      ), Q(
        e,
        "large",
        /*size*/
        l[0] === "large"
      ), Q(
        e,
        "unpadded_box",
        /*unpadded_box*/
        l[1]
      ), Q(
        e,
        "small_parent",
        /*parent_height*/
        l[3]
      );
    },
    m(s, f) {
      hl(s, e, f), _l(e, t), o && o.m(t, null), l[6](e), n = !0;
    },
    p(s, [f]) {
      o && o.p && (!n || f & /*$$scope*/
      16) && yl(
        o,
        i,
        s,
        /*$$scope*/
        s[4],
        n ? bl(
          i,
          /*$$scope*/
          s[4],
          f,
          null
        ) : ml(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!n || f & /*size*/
      1) && Q(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!n || f & /*size*/
      1) && Q(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!n || f & /*unpadded_box*/
      2) && Q(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!n || f & /*parent_height*/
      8) && Q(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      n || (kl(o, s), n = !0);
    },
    o(s) {
      pl(o, s), n = !1;
    },
    d(s) {
      s && dl(e), o && o.d(s), l[6](null);
    }
  };
}
function ql(l) {
  let e, t = l[0], n = 1;
  for (; n < l.length; ) {
    const i = l[n], o = l[n + 1];
    if (n += 2, (i === "optionalAccess" || i === "optionalCall") && t == null)
      return;
    i === "access" || i === "optionalAccess" ? (e = t, t = o(t)) : (i === "call" || i === "optionalCall") && (t = o((...s) => t.call(e, ...s)), e = void 0);
  }
  return t;
}
function Cl(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e, { size: s = "small" } = e, { unpadded_box: f = !1 } = e, a;
  function r(u) {
    if (!u)
      return !1;
    const { height: m } = u.getBoundingClientRect(), { height: g } = ql([
      u,
      "access",
      (c) => c.parentElement,
      "optionalAccess",
      (c) => c.getBoundingClientRect,
      "call",
      (c) => c()
    ]) || { height: m };
    return m > g + 2;
  }
  function _(u) {
    ul[u ? "unshift" : "push"](() => {
      a = u, t(2, a);
    });
  }
  return l.$$set = (u) => {
    "size" in u && t(0, s = u.size), "unpadded_box" in u && t(1, f = u.unpadded_box), "$$scope" in u && t(4, o = u.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*el*/
    4 && t(3, n = r(a));
  }, [s, f, a, n, o, i, _];
}
class Ll extends rl {
  constructor(e) {
    super(), gl(this, e, Cl, vl, wl, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: Fl,
  append: Pe,
  attr: z,
  detach: Sl,
  init: zl,
  insert: Ml,
  noop: Re,
  safe_not_equal: Vl,
  svg_element: ye
} = window.__gradio__svelte__internal;
function El(l) {
  let e, t, n, i;
  return {
    c() {
      e = ye("svg"), t = ye("rect"), n = ye("circle"), i = ye("polyline"), z(t, "x", "3"), z(t, "y", "3"), z(t, "width", "18"), z(t, "height", "18"), z(t, "rx", "2"), z(t, "ry", "2"), z(n, "cx", "8.5"), z(n, "cy", "8.5"), z(n, "r", "1.5"), z(i, "points", "21 15 16 10 5 21"), z(e, "xmlns", "http://www.w3.org/2000/svg"), z(e, "width", "100%"), z(e, "height", "100%"), z(e, "viewBox", "0 0 24 24"), z(e, "fill", "none"), z(e, "stroke", "currentColor"), z(e, "stroke-width", "1.5"), z(e, "stroke-linecap", "round"), z(e, "stroke-linejoin", "round"), z(e, "class", "feather feather-image");
    },
    m(o, s) {
      Ml(o, e, s), Pe(e, t), Pe(e, n), Pe(e, i);
    },
    p: Re,
    i: Re,
    o: Re,
    d(o) {
      o && Sl(e);
    }
  };
}
class vt extends Fl {
  constructor(e) {
    super(), zl(this, e, null, El, Vl, {});
  }
}
const Nl = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], De = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Nl.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: De[e][t],
      secondary: De[e][n]
    }
  }),
  {}
);
function oe(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Ce() {
}
function Pl(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const qt = typeof window < "u";
let Xe = qt ? () => window.performance.now() : () => Date.now(), Ct = qt ? (l) => requestAnimationFrame(l) : Ce;
const ae = /* @__PURE__ */ new Set();
function Lt(l) {
  ae.forEach((e) => {
    e.c(l) || (ae.delete(e), e.f());
  }), ae.size !== 0 && Ct(Lt);
}
function Rl(l) {
  let e;
  return ae.size === 0 && Ct(Lt), {
    promise: new Promise((t) => {
      ae.add(e = { c: l, f: t });
    }),
    abort() {
      ae.delete(e);
    }
  };
}
const se = [];
function Tl(l, e = Ce) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (Pl(l, f) && (l = f, t)) {
      const a = !se.length;
      for (const r of n)
        r[1](), se.push(r, l);
      if (a) {
        for (let r = 0; r < se.length; r += 2)
          se[r][0](se[r + 1]);
        se.length = 0;
      }
    }
  }
  function o(f) {
    i(f(l));
  }
  function s(f, a = Ce) {
    const r = [f, a];
    return n.add(r), n.size === 1 && (t = e(i, o) || Ce), f(l), () => {
      n.delete(r), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: s };
}
function Ye(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Be(l, e, t, n) {
  if (typeof t == "number" || Ye(t)) {
    const i = n - t, o = (t - e) / (l.dt || 1 / 60), s = l.opts.stiffness * i, f = l.opts.damping * o, a = (s - f) * l.inv_mass, r = (o + a) * l.dt;
    return Math.abs(r) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, Ye(t) ? new Date(t.getTime() + r) : t + r);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => Be(l, e[o], t[o], n[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = Be(l, e[o], t[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Ke(l, e = {}) {
  const t = Tl(l), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let s, f, a, r = l, _ = l, u = 1, m = 0, g = !1;
  function c(L, S = {}) {
    _ = L;
    const C = a = {};
    return l == null || S.hard || y.stiffness >= 1 && y.damping >= 1 ? (g = !0, s = Xe(), r = L, t.set(l = _), Promise.resolve()) : (S.soft && (m = 1 / ((S.soft === !0 ? 0.5 : +S.soft) * 60), u = 0), f || (s = Xe(), g = !1, f = Rl((d) => {
      if (g)
        return g = !1, f = null, !1;
      u = Math.min(u + m, 1);
      const v = {
        inv_mass: u,
        opts: y,
        settled: !0,
        dt: (d - s) * 60 / 1e3
      }, M = Be(v, r, l, _);
      return s = d, r = l, t.set(l = M), v.settled && (f = null), !v.settled;
    })), new Promise((d) => {
      f.promise.then(() => {
        C === a && d();
      });
    }));
  }
  const y = {
    set: c,
    update: (L, S) => c(L(_, l), S),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return y;
}
const {
  SvelteComponent: Al,
  append: A,
  attr: q,
  component_subscribe: We,
  detach: Bl,
  element: Il,
  init: jl,
  insert: Ol,
  noop: Ge,
  safe_not_equal: Zl,
  set_style: ve,
  svg_element: B,
  toggle_class: He
} = window.__gradio__svelte__internal, { onMount: Ul } = window.__gradio__svelte__internal;
function Dl(l) {
  let e, t, n, i, o, s, f, a, r, _, u, m;
  return {
    c() {
      e = Il("div"), t = B("svg"), n = B("g"), i = B("path"), o = B("path"), s = B("path"), f = B("path"), a = B("g"), r = B("path"), _ = B("path"), u = B("path"), m = B("path"), q(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), q(i, "fill", "#FF7C00"), q(i, "fill-opacity", "0.4"), q(i, "class", "svelte-43sxxs"), q(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), q(o, "fill", "#FF7C00"), q(o, "class", "svelte-43sxxs"), q(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), q(s, "fill", "#FF7C00"), q(s, "fill-opacity", "0.4"), q(s, "class", "svelte-43sxxs"), q(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), q(f, "fill", "#FF7C00"), q(f, "class", "svelte-43sxxs"), ve(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), q(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), q(r, "fill", "#FF7C00"), q(r, "fill-opacity", "0.4"), q(r, "class", "svelte-43sxxs"), q(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), q(_, "fill", "#FF7C00"), q(_, "class", "svelte-43sxxs"), q(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), q(u, "fill", "#FF7C00"), q(u, "fill-opacity", "0.4"), q(u, "class", "svelte-43sxxs"), q(m, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), q(m, "fill", "#FF7C00"), q(m, "class", "svelte-43sxxs"), ve(a, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), q(t, "viewBox", "-1200 -1200 3000 3000"), q(t, "fill", "none"), q(t, "xmlns", "http://www.w3.org/2000/svg"), q(t, "class", "svelte-43sxxs"), q(e, "class", "svelte-43sxxs"), He(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(g, c) {
      Ol(g, e, c), A(e, t), A(t, n), A(n, i), A(n, o), A(n, s), A(n, f), A(t, a), A(a, r), A(a, _), A(a, u), A(a, m);
    },
    p(g, [c]) {
      c & /*$top*/
      2 && ve(n, "transform", "translate(" + /*$top*/
      g[1][0] + "px, " + /*$top*/
      g[1][1] + "px)"), c & /*$bottom*/
      4 && ve(a, "transform", "translate(" + /*$bottom*/
      g[2][0] + "px, " + /*$bottom*/
      g[2][1] + "px)"), c & /*margin*/
      1 && He(
        e,
        "margin",
        /*margin*/
        g[0]
      );
    },
    i: Ge,
    o: Ge,
    d(g) {
      g && Bl(e);
    }
  };
}
function Xl(l, e, t) {
  let n, i, { margin: o = !0 } = e;
  const s = Ke([0, 0]);
  We(l, s, (m) => t(1, n = m));
  const f = Ke([0, 0]);
  We(l, f, (m) => t(2, i = m));
  let a;
  async function r() {
    await Promise.all([s.set([125, 140]), f.set([-125, -140])]), await Promise.all([s.set([-125, 140]), f.set([125, -140])]), await Promise.all([s.set([-125, 0]), f.set([125, -0])]), await Promise.all([s.set([125, 0]), f.set([-125, 0])]);
  }
  async function _() {
    await r(), a || _();
  }
  async function u() {
    await Promise.all([s.set([125, 0]), f.set([-125, 0])]), _();
  }
  return Ul(() => (u(), () => a = !0)), l.$$set = (m) => {
    "margin" in m && t(0, o = m.margin);
  }, [o, n, i, s, f];
}
class Yl extends Al {
  constructor(e) {
    super(), jl(this, e, Xl, Dl, Zl, { margin: 0 });
  }
}
const {
  SvelteComponent: Kl,
  append: ee,
  attr: j,
  binding_callbacks: Je,
  check_outros: Ft,
  create_component: Wl,
  create_slot: Gl,
  destroy_component: Hl,
  destroy_each: St,
  detach: k,
  element: X,
  empty: ce,
  ensure_array_like: Le,
  get_all_dirty_from_scope: Jl,
  get_slot_changes: Ql,
  group_outros: zt,
  init: xl,
  insert: p,
  mount_component: $l,
  noop: Ie,
  safe_not_equal: en,
  set_data: P,
  set_style: x,
  space: O,
  text: F,
  toggle_class: N,
  transition_in: re,
  transition_out: _e,
  update_slot_base: tn
} = window.__gradio__svelte__internal, { tick: ln } = window.__gradio__svelte__internal, { onDestroy: nn } = window.__gradio__svelte__internal, sn = (l) => ({}), Qe = (l) => ({});
function xe(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n[40] = t, n;
}
function $e(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n;
}
function on(l) {
  let e, t = (
    /*i18n*/
    l[1]("common.error") + ""
  ), n, i, o;
  const s = (
    /*#slots*/
    l[29].error
  ), f = Gl(
    s,
    l,
    /*$$scope*/
    l[28],
    Qe
  );
  return {
    c() {
      e = X("span"), n = F(t), i = O(), f && f.c(), j(e, "class", "error svelte-1txqlrd");
    },
    m(a, r) {
      p(a, e, r), ee(e, n), p(a, i, r), f && f.m(a, r), o = !0;
    },
    p(a, r) {
      (!o || r[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      a[1]("common.error") + "") && P(n, t), f && f.p && (!o || r[0] & /*$$scope*/
      268435456) && tn(
        f,
        s,
        a,
        /*$$scope*/
        a[28],
        o ? Ql(
          s,
          /*$$scope*/
          a[28],
          r,
          sn
        ) : Jl(
          /*$$scope*/
          a[28]
        ),
        Qe
      );
    },
    i(a) {
      o || (re(f, a), o = !0);
    },
    o(a) {
      _e(f, a), o = !1;
    },
    d(a) {
      a && (k(e), k(i)), f && f.d(a);
    }
  };
}
function fn(l) {
  let e, t, n, i, o, s, f, a, r, _ = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && et(l)
  );
  function u(d, v) {
    if (
      /*progress*/
      d[7]
    )
      return _n;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return rn;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return an;
  }
  let m = u(l), g = m && m(l), c = (
    /*timer*/
    l[5] && nt(l)
  );
  const y = [mn, dn], L = [];
  function S(d, v) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = S(l)) && (s = L[o] = y[o](l));
  let C = !/*timer*/
  l[5] && _t(l);
  return {
    c() {
      _ && _.c(), e = O(), t = X("div"), g && g.c(), n = O(), c && c.c(), i = O(), s && s.c(), f = O(), C && C.c(), a = ce(), j(t, "class", "progress-text svelte-1txqlrd"), N(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), N(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(d, v) {
      _ && _.m(d, v), p(d, e, v), p(d, t, v), g && g.m(t, null), ee(t, n), c && c.m(t, null), p(d, i, v), ~o && L[o].m(d, v), p(d, f, v), C && C.m(d, v), p(d, a, v), r = !0;
    },
    p(d, v) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? _ ? _.p(d, v) : (_ = et(d), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), m === (m = u(d)) && g ? g.p(d, v) : (g && g.d(1), g = m && m(d), g && (g.c(), g.m(t, n))), /*timer*/
      d[5] ? c ? c.p(d, v) : (c = nt(d), c.c(), c.m(t, null)) : c && (c.d(1), c = null), (!r || v[0] & /*variant*/
      256) && N(
        t,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!r || v[0] & /*variant*/
      256) && N(
        t,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let M = o;
      o = S(d), o === M ? ~o && L[o].p(d, v) : (s && (zt(), _e(L[M], 1, 1, () => {
        L[M] = null;
      }), Ft()), ~o ? (s = L[o], s ? s.p(d, v) : (s = L[o] = y[o](d), s.c()), re(s, 1), s.m(f.parentNode, f)) : s = null), /*timer*/
      d[5] ? C && (C.d(1), C = null) : C ? C.p(d, v) : (C = _t(d), C.c(), C.m(a.parentNode, a));
    },
    i(d) {
      r || (re(s), r = !0);
    },
    o(d) {
      _e(s), r = !1;
    },
    d(d) {
      d && (k(e), k(t), k(i), k(f), k(a)), _ && _.d(d), g && g.d(), c && c.d(), ~o && L[o].d(d), C && C.d(d);
    }
  };
}
function et(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = X("div"), j(e, "class", "eta-bar svelte-1txqlrd"), x(e, "transform", t);
    },
    m(n, i) {
      p(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && x(e, "transform", t);
    },
    d(n) {
      n && k(e);
    }
  };
}
function an(l) {
  let e;
  return {
    c() {
      e = F("processing |");
    },
    m(t, n) {
      p(t, e, n);
    },
    p: Ie,
    d(t) {
      t && k(e);
    }
  };
}
function rn(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, o, s;
  return {
    c() {
      e = F("queue: "), n = F(t), i = F("/"), o = F(
        /*queue_size*/
        l[3]
      ), s = F(" |");
    },
    m(f, a) {
      p(f, e, a), p(f, n, a), p(f, i, a), p(f, o, a), p(f, s, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && P(n, t), a[0] & /*queue_size*/
      8 && P(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (k(e), k(n), k(i), k(o), k(s));
    }
  };
}
function _n(l) {
  let e, t = Le(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = lt($e(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ce();
    },
    m(i, o) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, o);
      p(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = Le(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = $e(i, t, s);
          n[s] ? n[s].p(f, o) : (n[s] = lt(f), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && k(e), St(n, i);
    }
  };
}
function tt(l) {
  let e, t = (
    /*p*/
    l[38].unit + ""
  ), n, i, o = " ", s;
  function f(_, u) {
    return (
      /*p*/
      _[38].length != null ? cn : un
    );
  }
  let a = f(l), r = a(l);
  return {
    c() {
      r.c(), e = O(), n = F(t), i = F(" | "), s = F(o);
    },
    m(_, u) {
      r.m(_, u), p(_, e, u), p(_, n, u), p(_, i, u), p(_, s, u);
    },
    p(_, u) {
      a === (a = f(_)) && r ? r.p(_, u) : (r.d(1), r = a(_), r && (r.c(), r.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[38].unit + "") && P(n, t);
    },
    d(_) {
      _ && (k(e), k(n), k(i), k(s)), r.d(_);
    }
  };
}
function un(l) {
  let e = oe(
    /*p*/
    l[38].index || 0
  ) + "", t;
  return {
    c() {
      t = F(e);
    },
    m(n, i) {
      p(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = oe(
        /*p*/
        n[38].index || 0
      ) + "") && P(t, e);
    },
    d(n) {
      n && k(t);
    }
  };
}
function cn(l) {
  let e = oe(
    /*p*/
    l[38].index || 0
  ) + "", t, n, i = oe(
    /*p*/
    l[38].length
  ) + "", o;
  return {
    c() {
      t = F(e), n = F("/"), o = F(i);
    },
    m(s, f) {
      p(s, t, f), p(s, n, f), p(s, o, f);
    },
    p(s, f) {
      f[0] & /*progress*/
      128 && e !== (e = oe(
        /*p*/
        s[38].index || 0
      ) + "") && P(t, e), f[0] & /*progress*/
      128 && i !== (i = oe(
        /*p*/
        s[38].length
      ) + "") && P(o, i);
    },
    d(s) {
      s && (k(t), k(n), k(o));
    }
  };
}
function lt(l) {
  let e, t = (
    /*p*/
    l[38].index != null && tt(l)
  );
  return {
    c() {
      t && t.c(), e = ce();
    },
    m(n, i) {
      t && t.m(n, i), p(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[38].index != null ? t ? t.p(n, i) : (t = tt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && k(e), t && t.d(n);
    }
  };
}
function nt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = F(
        /*formatted_timer*/
        l[20]
      ), n = F(t), i = F("s");
    },
    m(o, s) {
      p(o, e, s), p(o, n, s), p(o, i, s);
    },
    p(o, s) {
      s[0] & /*formatted_timer*/
      1048576 && P(
        e,
        /*formatted_timer*/
        o[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && P(n, t);
    },
    d(o) {
      o && (k(e), k(n), k(i));
    }
  };
}
function dn(l) {
  let e, t;
  return e = new Yl({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Wl(e.$$.fragment);
    },
    m(n, i) {
      $l(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (re(e.$$.fragment, n), t = !0);
    },
    o(n) {
      _e(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Hl(e, n);
    }
  };
}
function mn(l) {
  let e, t, n, i, o, s = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && it(l)
  );
  return {
    c() {
      e = X("div"), t = X("div"), f && f.c(), n = O(), i = X("div"), o = X("div"), j(t, "class", "progress-level-inner svelte-1txqlrd"), j(o, "class", "progress-bar svelte-1txqlrd"), x(o, "width", s), j(i, "class", "progress-bar-wrap svelte-1txqlrd"), j(e, "class", "progress-level svelte-1txqlrd");
    },
    m(a, r) {
      p(a, e, r), ee(e, t), f && f.m(t, null), ee(e, n), ee(e, i), ee(i, o), l[30](o);
    },
    p(a, r) {
      /*progress*/
      a[7] != null ? f ? f.p(a, r) : (f = it(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), r[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      a[15] * 100}%`) && x(o, "width", s);
    },
    i: Ie,
    o: Ie,
    d(a) {
      a && k(e), f && f.d(), l[30](null);
    }
  };
}
function it(l) {
  let e, t = Le(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = rt(xe(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ce();
    },
    m(i, o) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, o);
      p(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = Le(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = xe(i, t, s);
          n[s] ? n[s].p(f, o) : (n[s] = rt(f), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && k(e), St(n, i);
    }
  };
}
function st(l) {
  let e, t, n, i, o = (
    /*i*/
    l[40] !== 0 && bn()
  ), s = (
    /*p*/
    l[38].desc != null && ot(l)
  ), f = (
    /*p*/
    l[38].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null && ft()
  ), a = (
    /*progress_level*/
    l[14] != null && at(l)
  );
  return {
    c() {
      o && o.c(), e = O(), s && s.c(), t = O(), f && f.c(), n = O(), a && a.c(), i = ce();
    },
    m(r, _) {
      o && o.m(r, _), p(r, e, _), s && s.m(r, _), p(r, t, _), f && f.m(r, _), p(r, n, _), a && a.m(r, _), p(r, i, _);
    },
    p(r, _) {
      /*p*/
      r[38].desc != null ? s ? s.p(r, _) : (s = ot(r), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      r[38].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[40]
      ] != null ? f || (f = ft(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      r[14] != null ? a ? a.p(r, _) : (a = at(r), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(r) {
      r && (k(e), k(t), k(n), k(i)), o && o.d(r), s && s.d(r), f && f.d(r), a && a.d(r);
    }
  };
}
function bn(l) {
  let e;
  return {
    c() {
      e = F(" /");
    },
    m(t, n) {
      p(t, e, n);
    },
    d(t) {
      t && k(e);
    }
  };
}
function ot(l) {
  let e = (
    /*p*/
    l[38].desc + ""
  ), t;
  return {
    c() {
      t = F(e);
    },
    m(n, i) {
      p(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[38].desc + "") && P(t, e);
    },
    d(n) {
      n && k(t);
    }
  };
}
function ft(l) {
  let e;
  return {
    c() {
      e = F("-");
    },
    m(t, n) {
      p(t, e, n);
    },
    d(t) {
      t && k(e);
    }
  };
}
function at(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[40]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = F(e), n = F("%");
    },
    m(i, o) {
      p(i, t, o), p(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && P(t, e);
    },
    d(i) {
      i && (k(t), k(n));
    }
  };
}
function rt(l) {
  let e, t = (
    /*p*/
    (l[38].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null) && st(l)
  );
  return {
    c() {
      t && t.c(), e = ce();
    },
    m(n, i) {
      t && t.m(n, i), p(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[38].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[40]
      ] != null ? t ? t.p(n, i) : (t = st(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && k(e), t && t.d(n);
    }
  };
}
function _t(l) {
  let e, t;
  return {
    c() {
      e = X("p"), t = F(
        /*loading_text*/
        l[9]
      ), j(e, "class", "loading svelte-1txqlrd");
    },
    m(n, i) {
      p(n, e, i), ee(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && P(
        t,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && k(e);
    }
  };
}
function gn(l) {
  let e, t, n, i, o;
  const s = [fn, on], f = [];
  function a(r, _) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(l)) && (n = f[t] = s[t](l)), {
    c() {
      e = X("div"), n && n.c(), j(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1txqlrd"), N(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), N(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), N(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), N(
        e,
        "border",
        /*border*/
        l[12]
      ), x(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), x(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, _) {
      p(r, e, _), ~t && f[t].m(e, null), l[31](e), o = !0;
    },
    p(r, _) {
      let u = t;
      t = a(r), t === u ? ~t && f[t].p(r, _) : (n && (zt(), _e(f[u], 1, 1, () => {
        f[u] = null;
      }), Ft()), ~t ? (n = f[t], n ? n.p(r, _) : (n = f[t] = s[t](r), n.c()), re(n, 1), n.m(e, null)) : n = null), (!o || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1txqlrd")) && j(e, "class", i), (!o || _[0] & /*variant, show_progress, status, show_progress*/
      336) && N(e, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!o || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && N(
        e,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!o || _[0] & /*variant, show_progress, status*/
      336) && N(
        e,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!o || _[0] & /*variant, show_progress, border*/
      4416) && N(
        e,
        "border",
        /*border*/
        r[12]
      ), _[0] & /*absolute*/
      1024 && x(
        e,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && x(
        e,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      o || (re(n), o = !0);
    },
    o(r) {
      _e(n), o = !1;
    },
    d(r) {
      r && k(e), ~t && f[t].d(), l[31](null);
    }
  };
}
let qe = [], Te = !1;
async function hn(l, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (qe.push(l), !Te)
      Te = !0;
    else
      return;
    await ln(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let n = 0; n < qe.length; n++) {
        const o = qe[n].getBoundingClientRect();
        (n === 0 || o.top + window.scrollY <= t[0]) && (t[0] = o.top + window.scrollY, t[1] = n);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Te = !1, qe = [];
    });
  }
}
function wn(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e, { i18n: s } = e, { eta: f = null } = e, { queue_position: a } = e, { queue_size: r } = e, { status: _ } = e, { scroll_to_output: u = !1 } = e, { timer: m = !0 } = e, { show_progress: g = "full" } = e, { message: c = null } = e, { progress: y = null } = e, { variant: L = "default" } = e, { loading_text: S = "Loading..." } = e, { absolute: C = !0 } = e, { translucent: d = !1 } = e, { border: v = !1 } = e, { autoscroll: M } = e, w, Z = !1, W = 0, R = 0, U = null, G = null, we = 0, D = null, $, I = null, b = !0;
  const ne = () => {
    t(0, f = t(26, U = t(19, T = null))), t(24, W = performance.now()), t(25, R = 0), Z = !0, ke();
  };
  function ke() {
    requestAnimationFrame(() => {
      t(25, R = (performance.now() - W) / 1e3), Z && ke();
    });
  }
  function ie() {
    t(25, R = 0), t(0, f = t(26, U = t(19, T = null))), Z && (Z = !1);
  }
  nn(() => {
    Z && ie();
  });
  let T = null;
  function Me(h) {
    Je[h ? "unshift" : "push"](() => {
      I = h, t(16, I), t(7, y), t(14, D), t(15, $);
    });
  }
  function Ve(h) {
    Je[h ? "unshift" : "push"](() => {
      w = h, t(13, w);
    });
  }
  return l.$$set = (h) => {
    "i18n" in h && t(1, s = h.i18n), "eta" in h && t(0, f = h.eta), "queue_position" in h && t(2, a = h.queue_position), "queue_size" in h && t(3, r = h.queue_size), "status" in h && t(4, _ = h.status), "scroll_to_output" in h && t(21, u = h.scroll_to_output), "timer" in h && t(5, m = h.timer), "show_progress" in h && t(6, g = h.show_progress), "message" in h && t(22, c = h.message), "progress" in h && t(7, y = h.progress), "variant" in h && t(8, L = h.variant), "loading_text" in h && t(9, S = h.loading_text), "absolute" in h && t(10, C = h.absolute), "translucent" in h && t(11, d = h.translucent), "border" in h && t(12, v = h.border), "autoscroll" in h && t(23, M = h.autoscroll), "$$scope" in h && t(28, o = h.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (f === null && t(0, f = U), f != null && U !== f && (t(27, G = (performance.now() - W) / 1e3 + f), t(19, T = G.toFixed(1)), t(26, U = f))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && t(17, we = G === null || G <= 0 || !R ? null : Math.min(R / G, 1)), l.$$.dirty[0] & /*progress*/
    128 && y != null && t(18, b = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (y != null ? t(14, D = y.map((h) => {
      if (h.index != null && h.length != null)
        return h.index / h.length;
      if (h.progress != null)
        return h.progress;
    })) : t(14, D = null), D ? (t(15, $ = D[D.length - 1]), I && ($ === 0 ? t(16, I.style.transition = "0", I) : t(16, I.style.transition = "150ms", I))) : t(15, $ = void 0)), l.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? ne() : ie()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && w && u && (_ === "pending" || _ === "complete") && hn(w, M), l.$$.dirty[0] & /*status, message*/
    4194320, l.$$.dirty[0] & /*timer_diff*/
    33554432 && t(20, n = R.toFixed(1));
  }, [
    f,
    s,
    a,
    r,
    _,
    m,
    g,
    y,
    L,
    S,
    C,
    d,
    v,
    w,
    D,
    $,
    I,
    we,
    b,
    T,
    n,
    u,
    c,
    M,
    W,
    R,
    U,
    G,
    o,
    i,
    Me,
    Ve
  ];
}
class kn extends Kl {
  constructor(e) {
    super(), xl(
      this,
      e,
      wn,
      gn,
      en,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
new Intl.Collator(0, { numeric: 1 }).compare;
function je(l, e, t) {
  if (l == null)
    return null;
  if (Array.isArray(l)) {
    const n = [];
    for (const i of l)
      i == null ? n.push(null) : n.push(je(i, e, t));
    return n;
  }
  return l.is_stream ? t == null ? new Ae({
    ...l,
    url: e + "/stream/" + l.path
  }) : new Ae({
    ...l,
    url: "/proxy=" + t + "stream/" + l.path
  }) : new Ae({
    ...l,
    url: yn(l.path, e, t)
  });
}
function pn(l) {
  try {
    const e = new URL(l);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function yn(l, e, t) {
  return l == null ? t ? `/proxy=${t}file=` : `${e}/file=` : pn(l) ? l : t ? `/proxy=${t}file=${l}` : `${e}/file=${l}`;
}
class Ae {
  constructor({
    path: e,
    url: t,
    orig_name: n,
    size: i,
    blob: o,
    is_stream: s,
    mime_type: f,
    alt_text: a
  }) {
    this.path = e, this.url = t, this.orig_name = n, this.size = i, this.blob = t ? void 0 : o, this.is_stream = s, this.mime_type = f, this.alt_text = a;
  }
}
const { setContext: Kn, getContext: vn } = window.__gradio__svelte__internal, qn = "WORKER_PROXY_CONTEXT_KEY";
function Cn() {
  return vn(qn);
}
function Ln(l) {
  return l.host === window.location.host || l.host === "localhost:7860" || l.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  l.host === "lite.local";
}
function Fn(l, e) {
  const t = e.toLowerCase();
  for (const [n, i] of Object.entries(l))
    if (n.toLowerCase() === t)
      return i;
}
function Sn(l) {
  if (l == null)
    return !1;
  const e = new URL(l);
  return !(!Ln(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
async function ut(l) {
  if (l == null || !Sn(l))
    return l;
  const e = Cn();
  if (e == null)
    return l;
  const n = new URL(l).pathname;
  return e.httpRequest({
    method: "GET",
    path: n,
    headers: {},
    query_string: ""
  }).then((i) => {
    if (i.status !== 200)
      throw new Error(`Failed to get file ${n} from the Wasm worker.`);
    const o = new Blob([i.body], {
      type: Fn(i.headers, "content-type")
    });
    return URL.createObjectURL(o);
  });
}
const {
  SvelteComponent: zn,
  append: Fe,
  assign: Mn,
  attr: V,
  check_outros: Vn,
  create_component: me,
  destroy_component: be,
  destroy_each: Mt,
  detach: Y,
  element: ue,
  empty: En,
  ensure_array_like: Se,
  get_spread_object: Nn,
  get_spread_update: Pn,
  group_outros: Rn,
  init: Tn,
  insert: K,
  listen: de,
  mount_component: ge,
  noop: ct,
  run_all: An,
  safe_not_equal: Bn,
  set_data: In,
  set_style: dt,
  space: he,
  src_url_equal: ze,
  text: jn,
  toggle_class: fe,
  transition_in: te,
  transition_out: le
} = window.__gradio__svelte__internal;
function mt(l, e, t) {
  const n = l.slice();
  return n[29] = e[t], n[31] = t, n;
}
function bt(l, e, t) {
  const n = l.slice();
  return n[29] = e[t], n[31] = t, n;
}
function On(l) {
  var _;
  let e, t, n, i, o, s, f = Se(
    /*_value*/
    l[14] ? (
      /*_value*/
      (_ = l[14]) == null ? void 0 : _.annotations
    ) : []
  ), a = [];
  for (let u = 0; u < f.length; u += 1)
    a[u] = gt(bt(l, f, u));
  let r = (
    /*show_legend*/
    l[6] && /*_value*/
    l[14] && ht(l)
  );
  return {
    c() {
      e = ue("div"), t = ue("img"), i = he();
      for (let u = 0; u < a.length; u += 1)
        a[u].c();
      o = he(), r && r.c(), s = En(), V(t, "class", "base-image svelte-tyskb7"), ze(t.src, n = /*_value*/
      l[14] ? (
        /*_value*/
        l[14].image.url
      ) : null) || V(t, "src", n), V(t, "alt", "the base file that is annotated"), fe(
        t,
        "fit-height",
        /*height*/
        l[7]
      ), V(e, "class", "image-container svelte-tyskb7");
    },
    m(u, m) {
      K(u, e, m), Fe(e, t), Fe(e, i);
      for (let g = 0; g < a.length; g += 1)
        a[g] && a[g].m(e, null);
      K(u, o, m), r && r.m(u, m), K(u, s, m);
    },
    p(u, m) {
      var g;
      if (m[0] & /*_value*/
      16384 && !ze(t.src, n = /*_value*/
      u[14] ? (
        /*_value*/
        u[14].image.url
      ) : null) && V(t, "src", n), m[0] & /*height*/
      128 && fe(
        t,
        "fit-height",
        /*height*/
        u[7]
      ), m[0] & /*label, _value, color_map, active*/
      49680) {
        f = Se(
          /*_value*/
          u[14] ? (
            /*_value*/
            (g = u[14]) == null ? void 0 : g.annotations
          ) : []
        );
        let c;
        for (c = 0; c < f.length; c += 1) {
          const y = bt(u, f, c);
          a[c] ? a[c].p(y, m) : (a[c] = gt(y), a[c].c(), a[c].m(e, null));
        }
        for (; c < a.length; c += 1)
          a[c].d(1);
        a.length = f.length;
      }
      /*show_legend*/
      u[6] && /*_value*/
      u[14] ? r ? r.p(u, m) : (r = ht(u), r.c(), r.m(s.parentNode, s)) : r && (r.d(1), r = null);
    },
    i: ct,
    o: ct,
    d(u) {
      u && (Y(e), Y(o), Y(s)), Mt(a, u), r && r.d(u);
    }
  };
}
function Zn(l) {
  let e, t;
  return e = new Ll({
    props: {
      size: "large",
      unpadded_box: !0,
      $$slots: { default: [Un] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      me(e.$$.fragment);
    },
    m(n, i) {
      ge(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[1] & /*$$scope*/
      4 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (te(e.$$.fragment, n), t = !0);
    },
    o(n) {
      le(e.$$.fragment, n), t = !1;
    },
    d(n) {
      be(e, n);
    }
  };
}
function gt(l) {
  let e, t, n, i;
  return {
    c() {
      var o;
      e = ue("img"), V(e, "alt", t = "segmentation mask identifying " + /*label*/
      l[4] + " within the uploaded file"), V(e, "class", "mask fit-height svelte-tyskb7"), ze(e.src, n = /*ann*/
      l[29].image.url) || V(e, "src", n), V(e, "style", i = /*color_map*/
      l[9] && /*ann*/
      l[29].label in /*color_map*/
      l[9] ? null : `filter: hue-rotate(${Math.round(
        /*i*/
        l[31] * 360 / /*_value*/
        ((o = l[14]) == null ? void 0 : o.annotations.length)
      )}deg);`), fe(
        e,
        "active",
        /*active*/
        l[15] == /*ann*/
        l[29].label
      ), fe(
        e,
        "inactive",
        /*active*/
        l[15] != /*ann*/
        l[29].label && /*active*/
        l[15] != null
      );
    },
    m(o, s) {
      K(o, e, s);
    },
    p(o, s) {
      var f;
      s[0] & /*label*/
      16 && t !== (t = "segmentation mask identifying " + /*label*/
      o[4] + " within the uploaded file") && V(e, "alt", t), s[0] & /*_value*/
      16384 && !ze(e.src, n = /*ann*/
      o[29].image.url) && V(e, "src", n), s[0] & /*color_map, _value*/
      16896 && i !== (i = /*color_map*/
      o[9] && /*ann*/
      o[29].label in /*color_map*/
      o[9] ? null : `filter: hue-rotate(${Math.round(
        /*i*/
        o[31] * 360 / /*_value*/
        ((f = o[14]) == null ? void 0 : f.annotations.length)
      )}deg);`) && V(e, "style", i), s[0] & /*active, _value*/
      49152 && fe(
        e,
        "active",
        /*active*/
        o[15] == /*ann*/
        o[29].label
      ), s[0] & /*active, _value*/
      49152 && fe(
        e,
        "inactive",
        /*active*/
        o[15] != /*ann*/
        o[29].label && /*active*/
        o[15] != null
      );
    },
    d(o) {
      o && Y(e);
    }
  };
}
function ht(l) {
  let e, t = Se(
    /*_value*/
    l[14].annotations
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = wt(mt(l, t, i));
  return {
    c() {
      e = ue("div");
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      V(e, "class", "legend svelte-tyskb7");
    },
    m(i, o) {
      K(i, e, o);
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(e, null);
    },
    p(i, o) {
      if (o[0] & /*color_map, _value, handle_mouseover, handle_mouseout, handle_click*/
      475648) {
        t = Se(
          /*_value*/
          i[14].annotations
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = mt(i, t, s);
          n[s] ? n[s].p(f, o) : (n[s] = wt(f), n[s].c(), n[s].m(e, null));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && Y(e), Mt(n, i);
    }
  };
}
function wt(l) {
  let e, t = (
    /*ann*/
    l[29].label + ""
  ), n, i, o, s;
  function f() {
    return (
      /*mouseover_handler*/
      l[24](
        /*ann*/
        l[29]
      )
    );
  }
  function a() {
    return (
      /*focus_handler*/
      l[25](
        /*ann*/
        l[29]
      )
    );
  }
  function r() {
    return (
      /*click_handler*/
      l[28](
        /*i*/
        l[31],
        /*ann*/
        l[29]
      )
    );
  }
  return {
    c() {
      e = ue("button"), n = jn(t), i = he(), V(e, "class", "legend-item svelte-tyskb7"), dt(
        e,
        "background-color",
        /*color_map*/
        l[9] && /*ann*/
        l[29].label in /*color_map*/
        l[9] ? (
          /*color_map*/
          l[9][
            /*ann*/
            l[29].label
          ] + "88"
        ) : `hsla(${Math.round(
          /*i*/
          l[31] * 360 / /*_value*/
          l[14].annotations.length
        )}, 100%, 50%, 0.3)`
      );
    },
    m(_, u) {
      K(_, e, u), Fe(e, n), Fe(e, i), o || (s = [
        de(e, "mouseover", f),
        de(e, "focus", a),
        de(
          e,
          "mouseout",
          /*mouseout_handler*/
          l[26]
        ),
        de(
          e,
          "blur",
          /*blur_handler*/
          l[27]
        ),
        de(e, "click", r)
      ], o = !0);
    },
    p(_, u) {
      l = _, u[0] & /*_value*/
      16384 && t !== (t = /*ann*/
      l[29].label + "") && In(n, t), u[0] & /*color_map, _value*/
      16896 && dt(
        e,
        "background-color",
        /*color_map*/
        l[9] && /*ann*/
        l[29].label in /*color_map*/
        l[9] ? (
          /*color_map*/
          l[9][
            /*ann*/
            l[29].label
          ] + "88"
        ) : `hsla(${Math.round(
          /*i*/
          l[31] * 360 / /*_value*/
          l[14].annotations.length
        )}, 100%, 50%, 0.3)`
      );
    },
    d(_) {
      _ && Y(e), o = !1, An(s);
    }
  };
}
function Un(l) {
  let e, t;
  return e = new vt({}), {
    c() {
      me(e.$$.fragment);
    },
    m(n, i) {
      ge(e, n, i), t = !0;
    },
    i(n) {
      t || (te(e.$$.fragment, n), t = !0);
    },
    o(n) {
      le(e.$$.fragment, n), t = !1;
    },
    d(n) {
      be(e, n);
    }
  };
}
function Dn(l) {
  let e, t, n, i, o, s, f, a;
  const r = [
    { autoscroll: (
      /*gradio*/
      l[3].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[3].i18n
    ) },
    /*loading_status*/
    l[13]
  ];
  let _ = {};
  for (let c = 0; c < r.length; c += 1)
    _ = Mn(_, r[c]);
  e = new kn({ props: _ }), n = new al({
    props: {
      show_label: (
        /*show_label*/
        l[5]
      ),
      Icon: vt,
      label: (
        /*label*/
        l[4] || /*gradio*/
        l[3].i18n("image.image")
      )
    }
  });
  const u = [Zn, On], m = [];
  function g(c, y) {
    return (
      /*_value*/
      c[14] == null ? 0 : 1
    );
  }
  return s = g(l), f = m[s] = u[s](l), {
    c() {
      me(e.$$.fragment), t = he(), me(n.$$.fragment), i = he(), o = ue("div"), f.c(), V(o, "class", "container svelte-tyskb7");
    },
    m(c, y) {
      ge(e, c, y), K(c, t, y), ge(n, c, y), K(c, i, y), K(c, o, y), m[s].m(o, null), a = !0;
    },
    p(c, y) {
      const L = y[0] & /*gradio, loading_status*/
      8200 ? Pn(r, [
        y[0] & /*gradio*/
        8 && { autoscroll: (
          /*gradio*/
          c[3].autoscroll
        ) },
        y[0] & /*gradio*/
        8 && { i18n: (
          /*gradio*/
          c[3].i18n
        ) },
        y[0] & /*loading_status*/
        8192 && Nn(
          /*loading_status*/
          c[13]
        )
      ]) : {};
      e.$set(L);
      const S = {};
      y[0] & /*show_label*/
      32 && (S.show_label = /*show_label*/
      c[5]), y[0] & /*label, gradio*/
      24 && (S.label = /*label*/
      c[4] || /*gradio*/
      c[3].i18n("image.image")), n.$set(S);
      let C = s;
      s = g(c), s === C ? m[s].p(c, y) : (Rn(), le(m[C], 1, 1, () => {
        m[C] = null;
      }), Vn(), f = m[s], f ? f.p(c, y) : (f = m[s] = u[s](c), f.c()), te(f, 1), f.m(o, null));
    },
    i(c) {
      a || (te(e.$$.fragment, c), te(n.$$.fragment, c), te(f), a = !0);
    },
    o(c) {
      le(e.$$.fragment, c), le(n.$$.fragment, c), le(f), a = !1;
    },
    d(c) {
      c && (Y(t), Y(i), Y(o)), be(e, c), be(n, c), m[s].d();
    }
  };
}
function Xn(l) {
  let e, t;
  return e = new Kt({
    props: {
      visible: (
        /*visible*/
        l[2]
      ),
      elem_id: (
        /*elem_id*/
        l[0]
      ),
      elem_classes: (
        /*elem_classes*/
        l[1]
      ),
      padding: !1,
      height: (
        /*height*/
        l[7]
      ),
      width: (
        /*width*/
        l[8]
      ),
      allow_overflow: !1,
      container: (
        /*container*/
        l[10]
      ),
      scale: (
        /*scale*/
        l[11]
      ),
      min_width: (
        /*min_width*/
        l[12]
      ),
      $$slots: { default: [Dn] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      me(e.$$.fragment);
    },
    m(n, i) {
      ge(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      4 && (o.visible = /*visible*/
      n[2]), i[0] & /*elem_id*/
      1 && (o.elem_id = /*elem_id*/
      n[0]), i[0] & /*elem_classes*/
      2 && (o.elem_classes = /*elem_classes*/
      n[1]), i[0] & /*height*/
      128 && (o.height = /*height*/
      n[7]), i[0] & /*width*/
      256 && (o.width = /*width*/
      n[8]), i[0] & /*container*/
      1024 && (o.container = /*container*/
      n[10]), i[0] & /*scale*/
      2048 && (o.scale = /*scale*/
      n[11]), i[0] & /*min_width*/
      4096 && (o.min_width = /*min_width*/
      n[12]), i[0] & /*_value, color_map, show_legend, label, active, height, show_label, gradio, loading_status*/
      58104 | i[1] & /*$$scope*/
      4 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (te(e.$$.fragment, n), t = !0);
    },
    o(n) {
      le(e.$$.fragment, n), t = !1;
    },
    d(n) {
      be(e, n);
    }
  };
}
function kt(l, e) {
  return l ?? e();
}
function Yn(l, e, t) {
  let { elem_id: n = "" } = e, { elem_classes: i = [] } = e, { visible: o = !0 } = e, { value: s = null } = e, f = null, a = null, { gradio: r } = e, { label: _ = r.i18n("annotated_image.annotated_image") } = e, { show_label: u = !0 } = e, { show_legend: m = !0 } = e, { height: g } = e, { width: c } = e, { color_map: y } = e, { container: L = !0 } = e, { scale: S = null } = e, { min_width: C = void 0 } = e, { root: d } = e, { proxy_url: v } = e, M = null, { loading_status: w } = e, Z = null;
  function W(b) {
    t(15, M = b);
  }
  function R() {
    t(15, M = null);
  }
  function U(b, ne) {
    r.dispatch("select", { value: _, index: b });
  }
  const G = (b) => W(b.label), we = (b) => W(b.label), D = () => R(), $ = () => R(), I = (b, ne) => U(b, ne.label);
  return l.$$set = (b) => {
    "elem_id" in b && t(0, n = b.elem_id), "elem_classes" in b && t(1, i = b.elem_classes), "visible" in b && t(2, o = b.visible), "value" in b && t(19, s = b.value), "gradio" in b && t(3, r = b.gradio), "label" in b && t(4, _ = b.label), "show_label" in b && t(5, u = b.show_label), "show_legend" in b && t(6, m = b.show_legend), "height" in b && t(7, g = b.height), "width" in b && t(8, c = b.width), "color_map" in b && t(9, y = b.color_map), "container" in b && t(10, L = b.container), "scale" in b && t(11, S = b.scale), "min_width" in b && t(12, C = b.min_width), "root" in b && t(20, d = b.root), "proxy_url" in b && t(21, v = b.proxy_url), "loading_status" in b && t(13, w = b.loading_status);
  }, l.$$.update = () => {
    if (l.$$.dirty[0] & /*value, old_value, gradio, root, proxy_url, latest_promise*/
    16252936)
      if (s !== f && (t(22, f = s), r.dispatch("change")), s) {
        const b = {
          image: je(s.image, d, v),
          annotations: s.annotations.map((T) => ({
            image: je(T.image, d, v),
            label: T.label
          }))
        };
        t(14, a = b);
        const ne = ut(b.image.url), ke = Promise.all(b.annotations.map((T) => ut(T.image.url))), ie = Promise.all([ne, ke]);
        t(23, Z = ie), ie.then(([T, Me]) => {
          if (Z !== ie)
            return;
          const Ve = {
            image: {
              ...b.image,
              url: kt(T, () => {
              })
            },
            annotations: b.annotations.map((h, Vt) => ({
              ...h,
              image: {
                ...h.image,
                url: kt(Me[Vt], () => {
                })
              }
            }))
          };
          t(14, a = Ve);
        });
      } else
        t(14, a = null);
  }, [
    n,
    i,
    o,
    r,
    _,
    u,
    m,
    g,
    c,
    y,
    L,
    S,
    C,
    w,
    a,
    M,
    W,
    R,
    U,
    s,
    d,
    v,
    f,
    Z,
    G,
    we,
    D,
    $,
    I
  ];
}
class Wn extends zn {
  constructor(e) {
    super(), Tn(
      this,
      e,
      Yn,
      Xn,
      Bn,
      {
        elem_id: 0,
        elem_classes: 1,
        visible: 2,
        value: 19,
        gradio: 3,
        label: 4,
        show_label: 5,
        show_legend: 6,
        height: 7,
        width: 8,
        color_map: 9,
        container: 10,
        scale: 11,
        min_width: 12,
        root: 20,
        proxy_url: 21,
        loading_status: 13
      },
      null,
      [-1, -1]
    );
  }
}
export {
  Wn as default
};
