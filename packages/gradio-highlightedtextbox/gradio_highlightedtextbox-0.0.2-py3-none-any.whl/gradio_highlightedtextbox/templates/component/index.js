const {
  SvelteComponent: nl,
  assign: il,
  create_slot: ol,
  detach: sl,
  element: fl,
  get_all_dirty_from_scope: rl,
  get_slot_changes: al,
  get_spread_update: _l,
  init: ul,
  insert: cl,
  safe_not_equal: dl,
  set_dynamic_element_data: et,
  set_style: A,
  toggle_class: te,
  transition_in: Ot,
  transition_out: It,
  update_slot_base: ml
} = window.__gradio__svelte__internal;
function bl(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), o = ol(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-1t38q2d"
    }
  ], r = {};
  for (let f = 0; f < s.length; f += 1)
    r = il(r, s[f]);
  return {
    c() {
      e = fl(
        /*tag*/
        n[14]
      ), o && o.c(), et(
        /*tag*/
        n[14]
      )(e, r), te(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), te(
        e,
        "padded",
        /*padding*/
        n[6]
      ), te(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), te(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), A(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), A(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), A(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), A(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), A(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), A(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), A(e, "border-width", "var(--block-border-width)");
    },
    m(f, a) {
      cl(f, e, a), o && o.m(e, null), l = !0;
    },
    p(f, a) {
      o && o.p && (!l || a & /*$$scope*/
      131072) && ml(
        o,
        i,
        f,
        /*$$scope*/
        f[17],
        l ? al(
          i,
          /*$$scope*/
          f[17],
          a,
          null
        ) : rl(
          /*$$scope*/
          f[17]
        ),
        null
      ), et(
        /*tag*/
        f[14]
      )(e, r = _l(s, [
        (!l || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!l || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!l || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), te(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), te(
        e,
        "padded",
        /*padding*/
        f[6]
      ), te(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), te(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), a & /*height*/
      1 && A(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), a & /*width*/
      2 && A(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), a & /*variant*/
      16 && A(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), a & /*allow_overflow*/
      2048 && A(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && A(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), a & /*min_width*/
      8192 && A(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      l || (Ot(o, f), l = !0);
    },
    o(f) {
      It(o, f), l = !1;
    },
    d(f) {
      f && sl(e), o && o.d(f);
    }
  };
}
function gl(n) {
  let e, t = (
    /*tag*/
    n[14] && bl(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (Ot(t, l), e = !0);
    },
    o(l) {
      It(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function hl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: s = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: f = [] } = e, { variant: a = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: c = "normal" } = e, { test_id: m = void 0 } = e, { explicit_call: p = !1 } = e, { container: T = !0 } = e, { visible: S = !0 } = e, { allow_overflow: L = !0 } = e, { scale: C = null } = e, { min_width: d = 0 } = e, y = c === "fieldset" ? "fieldset" : "div";
  const M = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return n.$$set = (g) => {
    "height" in g && t(0, o = g.height), "width" in g && t(1, s = g.width), "elem_id" in g && t(2, r = g.elem_id), "elem_classes" in g && t(3, f = g.elem_classes), "variant" in g && t(4, a = g.variant), "border_mode" in g && t(5, _ = g.border_mode), "padding" in g && t(6, u = g.padding), "type" in g && t(16, c = g.type), "test_id" in g && t(7, m = g.test_id), "explicit_call" in g && t(8, p = g.explicit_call), "container" in g && t(9, T = g.container), "visible" in g && t(10, S = g.visible), "allow_overflow" in g && t(11, L = g.allow_overflow), "scale" in g && t(12, C = g.scale), "min_width" in g && t(13, d = g.min_width), "$$scope" in g && t(17, i = g.$$scope);
  }, [
    o,
    s,
    r,
    f,
    a,
    _,
    u,
    m,
    p,
    T,
    S,
    L,
    C,
    d,
    y,
    M,
    c,
    i,
    l
  ];
}
class wl extends nl {
  constructor(e) {
    super(), ul(this, e, hl, gl, dl, {
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
  SvelteComponent: pl,
  attr: kl,
  create_slot: vl,
  detach: yl,
  element: Cl,
  get_all_dirty_from_scope: ql,
  get_slot_changes: Sl,
  init: Ll,
  insert: Tl,
  safe_not_equal: Fl,
  transition_in: Ml,
  transition_out: Nl,
  update_slot_base: Hl
} = window.__gradio__svelte__internal;
function jl(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = vl(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = Cl("div"), i && i.c(), kl(e, "class", "svelte-1hnfib2");
    },
    m(o, s) {
      Tl(o, e, s), i && i.m(e, null), t = !0;
    },
    p(o, [s]) {
      i && i.p && (!t || s & /*$$scope*/
      1) && Hl(
        i,
        l,
        o,
        /*$$scope*/
        o[0],
        t ? Sl(
          l,
          /*$$scope*/
          o[0],
          s,
          null
        ) : ql(
          /*$$scope*/
          o[0]
        ),
        null
      );
    },
    i(o) {
      t || (Ml(i, o), t = !0);
    },
    o(o) {
      Nl(i, o), t = !1;
    },
    d(o) {
      o && yl(e), i && i.d(o);
    }
  };
}
function Vl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (o) => {
    "$$scope" in o && t(0, i = o.$$scope);
  }, [i, l];
}
class Al extends pl {
  constructor(e) {
    super(), Ll(this, e, Vl, jl, Fl, {});
  }
}
const {
  SvelteComponent: zl,
  attr: tt,
  check_outros: El,
  create_component: Pl,
  create_slot: Zl,
  destroy_component: Bl,
  detach: je,
  element: Rl,
  empty: Dl,
  get_all_dirty_from_scope: Ol,
  get_slot_changes: Il,
  group_outros: Ul,
  init: Wl,
  insert: Ve,
  mount_component: Xl,
  safe_not_equal: Yl,
  set_data: Gl,
  space: Jl,
  text: Kl,
  toggle_class: ge,
  transition_in: Se,
  transition_out: Ae,
  update_slot_base: Ql
} = window.__gradio__svelte__internal;
function lt(n) {
  let e, t;
  return e = new Al({
    props: {
      $$slots: { default: [xl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Pl(e.$$.fragment);
    },
    m(l, i) {
      Xl(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*$$scope, info*/
      10 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (Se(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Ae(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Bl(e, l);
    }
  };
}
function xl(n) {
  let e;
  return {
    c() {
      e = Kl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      Ve(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Gl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && je(e);
    }
  };
}
function $l(n) {
  let e, t, l, i;
  const o = (
    /*#slots*/
    n[2].default
  ), s = Zl(
    o,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && lt(n)
  );
  return {
    c() {
      e = Rl("span"), s && s.c(), t = Jl(), r && r.c(), l = Dl(), tt(e, "data-testid", "block-info"), tt(e, "class", "svelte-22c38v"), ge(e, "sr-only", !/*show_label*/
      n[0]), ge(e, "hide", !/*show_label*/
      n[0]), ge(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(f, a) {
      Ve(f, e, a), s && s.m(e, null), Ve(f, t, a), r && r.m(f, a), Ve(f, l, a), i = !0;
    },
    p(f, [a]) {
      s && s.p && (!i || a & /*$$scope*/
      8) && Ql(
        s,
        o,
        f,
        /*$$scope*/
        f[3],
        i ? Il(
          o,
          /*$$scope*/
          f[3],
          a,
          null
        ) : Ol(
          /*$$scope*/
          f[3]
        ),
        null
      ), (!i || a & /*show_label*/
      1) && ge(e, "sr-only", !/*show_label*/
      f[0]), (!i || a & /*show_label*/
      1) && ge(e, "hide", !/*show_label*/
      f[0]), (!i || a & /*info*/
      2) && ge(
        e,
        "has-info",
        /*info*/
        f[1] != null
      ), /*info*/
      f[1] ? r ? (r.p(f, a), a & /*info*/
      2 && Se(r, 1)) : (r = lt(f), r.c(), Se(r, 1), r.m(l.parentNode, l)) : r && (Ul(), Ae(r, 1, 1, () => {
        r = null;
      }), El());
    },
    i(f) {
      i || (Se(s, f), Se(r), i = !0);
    },
    o(f) {
      Ae(s, f), Ae(r), i = !1;
    },
    d(f) {
      f && (je(e), je(t), je(l)), s && s.d(f), r && r.d(f);
    }
  };
}
function en(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: o = !0 } = e, { info: s = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, o = r.show_label), "info" in r && t(1, s = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [o, s, l, i];
}
class tn extends zl {
  constructor(e) {
    super(), Wl(this, e, en, $l, Yl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: ln,
  append: nn,
  attr: le,
  detach: on,
  init: sn,
  insert: fn,
  noop: Be,
  safe_not_equal: rn,
  svg_element: nt
} = window.__gradio__svelte__internal;
function an(n) {
  let e, t;
  return {
    c() {
      e = nt("svg"), t = nt("polyline"), le(t, "points", "20 6 9 17 4 12"), le(e, "xmlns", "http://www.w3.org/2000/svg"), le(e, "viewBox", "2 0 20 20"), le(e, "fill", "none"), le(e, "stroke", "currentColor"), le(e, "stroke-width", "3"), le(e, "stroke-linecap", "round"), le(e, "stroke-linejoin", "round");
    },
    m(l, i) {
      fn(l, e, i), nn(e, t);
    },
    p: Be,
    i: Be,
    o: Be,
    d(l) {
      l && on(e);
    }
  };
}
class _n extends ln {
  constructor(e) {
    super(), sn(this, e, null, an, rn, {});
  }
}
const {
  SvelteComponent: un,
  append: it,
  attr: ae,
  detach: cn,
  init: dn,
  insert: mn,
  noop: Re,
  safe_not_equal: bn,
  svg_element: De
} = window.__gradio__svelte__internal;
function gn(n) {
  let e, t, l;
  return {
    c() {
      e = De("svg"), t = De("path"), l = De("path"), ae(t, "fill", "currentColor"), ae(t, "d", "M28 10v18H10V10h18m0-2H10a2 2 0 0 0-2 2v18a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2Z"), ae(l, "fill", "currentColor"), ae(l, "d", "M4 18H2V4a2 2 0 0 1 2-2h14v2H4Z"), ae(e, "xmlns", "http://www.w3.org/2000/svg"), ae(e, "viewBox", "0 0 33 33"), ae(e, "color", "currentColor");
    },
    m(i, o) {
      mn(i, e, o), it(e, t), it(e, l);
    },
    p: Re,
    i: Re,
    o: Re,
    d(i) {
      i && cn(e);
    }
  };
}
class hn extends un {
  constructor(e) {
    super(), dn(this, e, null, gn, bn, {});
  }
}
const ot = [
  "red",
  "green",
  "blue",
  "yellow",
  "purple",
  "teal",
  "orange",
  "cyan",
  "lime",
  "pink"
], wn = [
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
], st = {
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
}, ft = wn.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: st[e][t],
      secondary: st[e][l]
    }
  }),
  {}
), pn = (n) => ot[n % ot.length];
function ze() {
}
const kn = (n) => n;
function vn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Ut = typeof window < "u";
let rt = Ut ? () => window.performance.now() : () => Date.now(), Wt = Ut ? (n) => requestAnimationFrame(n) : ze;
const ve = /* @__PURE__ */ new Set();
function Xt(n) {
  ve.forEach((e) => {
    e.c(n) || (ve.delete(e), e.f());
  }), ve.size !== 0 && Wt(Xt);
}
function yn(n) {
  let e;
  return ve.size === 0 && Wt(Xt), {
    promise: new Promise((t) => {
      ve.add(e = { c: n, f: t });
    }),
    abort() {
      ve.delete(e);
    }
  };
}
function Cn(n, { delay: e = 0, duration: t = 400, easing: l = kn } = {}) {
  const i = +getComputedStyle(n).opacity;
  return {
    delay: e,
    duration: t,
    easing: l,
    css: (o) => `opacity: ${o * i}`
  };
}
const he = [];
function qn(n, e = ze) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(r) {
    if (vn(n, r) && (n = r, t)) {
      const f = !he.length;
      for (const a of l)
        a[1](), he.push(a, n);
      if (f) {
        for (let a = 0; a < he.length; a += 2)
          he[a][0](he[a + 1]);
        he.length = 0;
      }
    }
  }
  function o(r) {
    i(r(n));
  }
  function s(r, f = ze) {
    const a = [r, f];
    return l.add(a), l.size === 1 && (t = e(i, o) || ze), r(n), () => {
      l.delete(a), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: s };
}
function at(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Ie(n, e, t, l) {
  if (typeof t == "number" || at(t)) {
    const i = l - t, o = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, r = n.opts.damping * o, f = (s - r) * n.inv_mass, a = (o + f) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, at(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => Ie(n, e[o], t[o], l[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = Ie(n, e[o], t[o], l[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function _t(n, e = {}) {
  const t = qn(n), { stiffness: l = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let s, r, f, a = n, _ = n, u = 1, c = 0, m = !1;
  function p(S, L = {}) {
    _ = S;
    const C = f = {};
    return n == null || L.hard || T.stiffness >= 1 && T.damping >= 1 ? (m = !0, s = rt(), a = S, t.set(n = _), Promise.resolve()) : (L.soft && (c = 1 / ((L.soft === !0 ? 0.5 : +L.soft) * 60), u = 0), r || (s = rt(), m = !1, r = yn((d) => {
      if (m)
        return m = !1, r = null, !1;
      u = Math.min(u + c, 1);
      const y = {
        inv_mass: u,
        opts: T,
        settled: !0,
        dt: (d - s) * 60 / 1e3
      }, M = Ie(y, a, n, _);
      return s = d, a = n, t.set(n = M), y.settled && (r = null), !y.settled;
    })), new Promise((d) => {
      r.promise.then(() => {
        C === f && d();
      });
    }));
  }
  const T = {
    set: p,
    update: (S, L) => p(S(_, n), L),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: o
  };
  return T;
}
function ut(n, e, t) {
  if (!t) {
    var l = document.createElement("canvas");
    t = l.getContext("2d");
  }
  t.fillStyle = n, t.fillRect(0, 0, 1, 1);
  const [i, o, s] = t.getImageData(0, 0, 1, 1).data;
  return t.clearRect(0, 0, 1, 1), `rgba(${i}, ${o}, ${s}, ${255 / e})`;
}
function Sn(n, e, t) {
  var l = {};
  for (const i in n) {
    const o = n[i].trim();
    o in ft ? l[i] = ft[o] : l[i] = {
      primary: e ? ut(n[i], 1, t) : n[i],
      secondary: e ? ut(n[i], 0.5, t) : n[i]
    };
  }
  return l;
}
function Ln(n, e) {
  let t = [], l = null, i = null;
  for (const [o, s] of n)
    e === "empty" && s === null || e === "equal" && i === s ? l = l ? l + o : o : (l !== null && t.push([l, i]), l = o, i = s);
  return l !== null && t.push([l, i]), t;
}
function Tn(n) {
  const e = window.getSelection();
  if (e.rangeCount > 0) {
    const t = document.createRange();
    return t.setStart(n, 0), e.anchorNode !== null && t.setEnd(e.anchorNode, e.anchorOffset), t.toString().length;
  }
  return -1;
}
function Fn(n, e) {
  var t = document.createTreeWalker(n, NodeFilter.SHOW_TEXT), l = t.nextNode();
  if (!l || !l.textContent)
    return null;
  for (var i = l.textContent.length; i < e; )
    if (l = t.nextNode(), l && l.textContent)
      i += l.textContent.length;
    else
      return null;
  var o = l.textContent.length - (i - e);
  return { node: l, offset: o };
}
const {
  SvelteComponent: Mn,
  add_render_callback: We,
  append: ue,
  attr: H,
  binding_callbacks: ct,
  bubble: we,
  check_outros: Yt,
  create_component: Xe,
  create_in_transition: Nn,
  destroy_component: Ye,
  destroy_each: Hn,
  detach: J,
  element: oe,
  empty: jn,
  ensure_array_like: dt,
  group_outros: Gt,
  init: Vn,
  insert: K,
  listen: V,
  mount_component: Ge,
  noop: Jt,
  run_all: An,
  safe_not_equal: zn,
  set_data: Je,
  space: Le,
  text: Ke,
  toggle_class: mt,
  transition_in: ne,
  transition_out: ce
} = window.__gradio__svelte__internal, { beforeUpdate: En, afterUpdate: Pn, createEventDispatcher: Zn, tick: Wi } = window.__gradio__svelte__internal;
function bt(n, e, t) {
  const l = n.slice();
  return l[40] = e[t][0], l[41] = e[t][1], l[43] = t, l;
}
function gt(n) {
  let e, t, l = (
    /*show_legend_label*/
    n[5] && ht(n)
  ), i = dt(Object.entries(
    /*_color_map*/
    n[12]
  )), o = [];
  for (let s = 0; s < i.length; s += 1)
    o[s] = wt(bt(n, i, s));
  return {
    c() {
      e = oe("div"), l && l.c(), t = Le();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      H(e, "class", "category-legend svelte-1u11ied"), H(e, "data-testid", "highlighted-text:category-legend");
    },
    m(s, r) {
      K(s, e, r), l && l.m(e, null), ue(e, t);
      for (let f = 0; f < o.length; f += 1)
        o[f] && o[f].m(e, null);
    },
    p(s, r) {
      if (/*show_legend_label*/
      s[5] ? l ? l.p(s, r) : (l = ht(s), l.c(), l.m(e, t)) : l && (l.d(1), l = null), r[0] & /*_color_map*/
      4096) {
        i = dt(Object.entries(
          /*_color_map*/
          s[12]
        ));
        let f;
        for (f = 0; f < i.length; f += 1) {
          const a = bt(s, i, f);
          o[f] ? o[f].p(a, r) : (o[f] = wt(a), o[f].c(), o[f].m(e, null));
        }
        for (; f < o.length; f += 1)
          o[f].d(1);
        o.length = i.length;
      }
    },
    d(s) {
      s && J(e), l && l.d(), Hn(o, s);
    }
  };
}
function ht(n) {
  let e, t;
  return {
    c() {
      e = oe("div"), t = Ke(
        /*legend_label*/
        n[1]
      ), H(e, "class", "legend-description svelte-1u11ied");
    },
    m(l, i) {
      K(l, e, i), ue(e, t);
    },
    p(l, i) {
      i[0] & /*legend_label*/
      2 && Je(
        t,
        /*legend_label*/
        l[1]
      );
    },
    d(l) {
      l && J(e);
    }
  };
}
function wt(n) {
  let e, t = (
    /*category*/
    n[40] + ""
  ), l, i, o;
  return {
    c() {
      e = oe("div"), l = Ke(t), i = Le(), H(e, "class", "category-label svelte-1u11ied"), H(e, "style", o = "background-color:" + /*color*/
      n[41].secondary);
    },
    m(s, r) {
      K(s, e, r), ue(e, l), ue(e, i);
    },
    p(s, r) {
      r[0] & /*_color_map*/
      4096 && t !== (t = /*category*/
      s[40] + "") && Je(l, t), r[0] & /*_color_map*/
      4096 && o !== (o = "background-color:" + /*color*/
      s[41].secondary) && H(e, "style", o);
    },
    d(s) {
      s && J(e);
    }
  };
}
function Bn(n) {
  let e;
  return {
    c() {
      e = Ke(
        /*label*/
        n[0]
      );
    },
    m(t, l) {
      K(t, e, l);
    },
    p(t, l) {
      l[0] & /*label*/
      1 && Je(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && J(e);
    }
  };
}
function pt(n) {
  let e, t, l, i;
  const o = [Dn, Rn], s = [];
  function r(f, a) {
    return (
      /*copied*/
      f[13] ? 0 : 1
    );
  }
  return e = r(n), t = s[e] = o[e](n), {
    c() {
      t.c(), l = jn();
    },
    m(f, a) {
      s[e].m(f, a), K(f, l, a), i = !0;
    },
    p(f, a) {
      let _ = e;
      e = r(f), e === _ ? s[e].p(f, a) : (Gt(), ce(s[_], 1, 1, () => {
        s[_] = null;
      }), Yt(), t = s[e], t ? t.p(f, a) : (t = s[e] = o[e](f), t.c()), ne(t, 1), t.m(l.parentNode, l));
    },
    i(f) {
      i || (ne(t), i = !0);
    },
    o(f) {
      ce(t), i = !1;
    },
    d(f) {
      f && J(l), s[e].d(f);
    }
  };
}
function Rn(n) {
  let e, t, l, i, o;
  return t = new hn({}), {
    c() {
      e = oe("button"), Xe(t.$$.fragment), H(e, "aria-label", "Copy"), H(e, "aria-roledescription", "Copy text"), H(e, "class", "svelte-1u11ied");
    },
    m(s, r) {
      K(s, e, r), Ge(t, e, null), l = !0, i || (o = V(
        e,
        "click",
        /*handle_copy*/
        n[15]
      ), i = !0);
    },
    p: Jt,
    i(s) {
      l || (ne(t.$$.fragment, s), l = !0);
    },
    o(s) {
      ce(t.$$.fragment, s), l = !1;
    },
    d(s) {
      s && J(e), Ye(t), i = !1, o();
    }
  };
}
function Dn(n) {
  let e, t, l, i;
  return t = new _n({}), {
    c() {
      e = oe("button"), Xe(t.$$.fragment), H(e, "aria-label", "Copied"), H(e, "aria-roledescription", "Text copied"), H(e, "class", "svelte-1u11ied");
    },
    m(o, s) {
      K(o, e, s), Ge(t, e, null), i = !0;
    },
    p: Jt,
    i(o) {
      i || (ne(t.$$.fragment, o), o && (l || We(() => {
        l = Nn(e, Cn, { duration: 300 }), l.start();
      })), i = !0);
    },
    o(o) {
      ce(t.$$.fragment, o), i = !1;
    },
    d(o) {
      o && J(e), Ye(t);
    }
  };
}
function On(n) {
  let e, t, l;
  return {
    c() {
      e = oe("div"), H(e, "class", "textfield svelte-1u11ied"), H(e, "data-testid", "highlighted-textbox"), H(e, "contenteditable", "true"), /*el_text*/
      (n[11] === void 0 || /*marked_el_text*/
      n[9] === void 0) && We(() => (
        /*div_input_handler_1*/
        n[29].call(e)
      ));
    },
    m(i, o) {
      K(i, e, o), n[28](e), /*el_text*/
      n[11] !== void 0 && (e.textContent = /*el_text*/
      n[11]), /*marked_el_text*/
      n[9] !== void 0 && (e.innerHTML = /*marked_el_text*/
      n[9]), t || (l = [
        V(
          e,
          "input",
          /*div_input_handler_1*/
          n[29]
        ),
        V(
          e,
          "blur",
          /*handle_blur*/
          n[14]
        ),
        V(
          e,
          "keypress",
          /*keypress_handler*/
          n[20]
        ),
        V(
          e,
          "select",
          /*select_handler*/
          n[21]
        ),
        V(
          e,
          "scroll",
          /*scroll_handler*/
          n[22]
        ),
        V(
          e,
          "input",
          /*input_handler*/
          n[23]
        ),
        V(
          e,
          "focus",
          /*focus_handler*/
          n[24]
        ),
        V(
          e,
          "change",
          /*change_handler*/
          n[25]
        ),
        V(
          e,
          "mousedown",
          /*checkAndRemoveHighlight*/
          n[16]
        ),
        V(
          e,
          "keydown",
          /*checkAndRemoveHighlight*/
          n[16]
        ),
        V(
          e,
          "mouseup",
          /*checkAndRemoveHighlight*/
          n[16]
        ),
        V(
          e,
          "keyup",
          /*checkAndRemoveHighlight*/
          n[16]
        )
      ], t = !0);
    },
    p(i, o) {
      o[0] & /*el_text*/
      2048 && /*el_text*/
      i[11] !== e.textContent && (e.textContent = /*el_text*/
      i[11]), o[0] & /*marked_el_text*/
      512 && /*marked_el_text*/
      i[9] !== e.innerHTML && (e.innerHTML = /*marked_el_text*/
      i[9]);
    },
    d(i) {
      i && J(e), n[28](null), t = !1, An(l);
    }
  };
}
function In(n) {
  let e, t, l;
  return {
    c() {
      e = oe("div"), H(e, "class", "textfield svelte-1u11ied"), H(e, "data-testid", "highlighted-textbox"), H(e, "contenteditable", "false"), /*el_text*/
      (n[11] === void 0 || /*marked_el_text*/
      n[9] === void 0) && We(() => (
        /*div_input_handler*/
        n[27].call(e)
      ));
    },
    m(i, o) {
      K(i, e, o), n[26](e), /*el_text*/
      n[11] !== void 0 && (e.textContent = /*el_text*/
      n[11]), /*marked_el_text*/
      n[9] !== void 0 && (e.innerHTML = /*marked_el_text*/
      n[9]), t || (l = V(
        e,
        "input",
        /*div_input_handler*/
        n[27]
      ), t = !0);
    },
    p(i, o) {
      o[0] & /*el_text*/
      2048 && /*el_text*/
      i[11] !== e.textContent && (e.textContent = /*el_text*/
      i[11]), o[0] & /*marked_el_text*/
      512 && /*marked_el_text*/
      i[9] !== e.innerHTML && (e.innerHTML = /*marked_el_text*/
      i[9]);
    },
    d(i) {
      i && J(e), n[26](null), t = !1, l();
    }
  };
}
function Un(n) {
  let e, t, l, i, o, s, r = (
    /*show_legend*/
    n[4] && gt(n)
  );
  l = new tn({
    props: {
      show_label: (
        /*show_label*/
        n[3]
      ),
      info: (
        /*info*/
        n[2]
      ),
      $$slots: { default: [Bn] },
      $$scope: { ctx: n }
    }
  });
  let f = (
    /*show_copy_button*/
    n[7] && pt(n)
  );
  function a(c, m) {
    return (
      /*disabled*/
      c[8] ? In : On
    );
  }
  let _ = a(n), u = _(n);
  return {
    c() {
      e = oe("label"), r && r.c(), t = Le(), Xe(l.$$.fragment), i = Le(), f && f.c(), o = Le(), u.c(), H(e, "class", "svelte-1u11ied"), mt(
        e,
        "container",
        /*container*/
        n[6]
      );
    },
    m(c, m) {
      K(c, e, m), r && r.m(e, null), ue(e, t), Ge(l, e, null), ue(e, i), f && f.m(e, null), ue(e, o), u.m(e, null), s = !0;
    },
    p(c, m) {
      /*show_legend*/
      c[4] ? r ? r.p(c, m) : (r = gt(c), r.c(), r.m(e, t)) : r && (r.d(1), r = null);
      const p = {};
      m[0] & /*show_label*/
      8 && (p.show_label = /*show_label*/
      c[3]), m[0] & /*info*/
      4 && (p.info = /*info*/
      c[2]), m[0] & /*label*/
      1 | m[1] & /*$$scope*/
      8192 && (p.$$scope = { dirty: m, ctx: c }), l.$set(p), /*show_copy_button*/
      c[7] ? f ? (f.p(c, m), m[0] & /*show_copy_button*/
      128 && ne(f, 1)) : (f = pt(c), f.c(), ne(f, 1), f.m(e, o)) : f && (Gt(), ce(f, 1, 1, () => {
        f = null;
      }), Yt()), _ === (_ = a(c)) && u ? u.p(c, m) : (u.d(1), u = _(c), u && (u.c(), u.m(e, null))), (!s || m[0] & /*container*/
      64) && mt(
        e,
        "container",
        /*container*/
        c[6]
      );
    },
    i(c) {
      s || (ne(l.$$.fragment, c), ne(f), s = !0);
    },
    o(c) {
      ce(l.$$.fragment, c), ce(f), s = !1;
    },
    d(c) {
      c && J(e), r && r.d(), Ye(l), f && f.d(), u.d();
    }
  };
}
function Wn(n) {
  let e, t = n[0], l = 1;
  for (; l < n.length; ) {
    const i = n[l], o = n[l + 1];
    if (l += 2, (i === "optionalAccess" || i === "optionalCall") && t == null)
      return;
    i === "access" || i === "optionalAccess" ? (e = t, t = o(t)) : (i === "call" || i === "optionalCall") && (t = o((...s) => t.call(e, ...s)), e = void 0);
  }
  return t;
}
function Xn(n, e, t) {
  const l = typeof document < "u";
  let { value: i = [] } = e, { value_is_output: o = !1 } = e, { label: s } = e, { legend_label: r } = e, { info: f = void 0 } = e, { show_label: a = !0 } = e, { show_legend: _ = !1 } = e, { show_legend_label: u = !1 } = e, { container: c = !0 } = e, { color_map: m = {} } = e, { show_copy_button: p = !1 } = e, { disabled: T } = e, S, L = "", C = "", d, y = {}, M = {}, g = !1, R;
  function Q() {
    if (!m || Object.keys(m).length === 0 ? y = {} : y = m, i.length > 0) {
      for (let [b, j] of i)
        if (j !== null && !(j in y)) {
          let P = pn(Object.keys(y).length);
          y[j] = P;
        }
    }
    t(12, M = Sn(y, l, d));
  }
  function z() {
    i.length > 0 && o && (t(11, L = i.map(([b, j]) => b).join(" ")), t(9, C = i.map(([b, j]) => j !== null ? `<mark class="hl ${j}" style="background-color:${M[j].secondary}">${b}</mark>` : b).join(" ") + " "));
  }
  const D = Zn();
  En(() => {
    S && S.offsetHeight + S.scrollTop > S.scrollHeight - 100;
  });
  function W() {
    D("change", C), o || D("input");
  }
  Pn(() => {
    Q(), z(), t(18, o = !1);
  });
  function se() {
    let b = [], j = "", P = null, ee = !1, be = "";
    for (let fe = 0; fe < C.length; fe++) {
      let re = C[fe];
      re === "<" ? (ee = !0, j && b.push([j, P]), j = "", P = null) : re === ">" ? (ee = !1, be.startsWith("mark") && (P = Wn([
        be,
        "access",
        (X) => X.match,
        "call",
        (X) => X(/class="hl ([^"]+)"/),
        "optionalAccess",
        (X) => X[1]
      ]) || null), be = "") : ee ? be += re : j += re;
    }
    j && b.push([j, P]), t(17, i = b);
  }
  async function O() {
    "clipboard" in navigator && (await navigator.clipboard.writeText(L), x());
  }
  function x() {
    t(13, g = !0), R && clearTimeout(R), R = setTimeout(
      () => {
        t(13, g = !1);
      },
      1e3
    );
  }
  function E() {
    const b = window.getSelection(), j = b.anchorOffset;
    if (b.rangeCount > 0) {
      var P = b.getRangeAt(0).commonAncestorContainer.parentElement;
      if (P && P.tagName.toLowerCase() === "mark") {
        const tl = P.textContent;
        var ee = P.parentElement, be = document.createTextNode(tl);
        ee.replaceChild(be, P), t(9, C = ee.innerHTML);
        var fe = document.createRange(), re = window.getSelection();
        const ll = j + Tn(ee);
        var X = Fn(ee, ll);
        fe.setStart(X.node, X.offset), fe.setEnd(X.node, X.offset), re.removeAllRanges(), re.addRange(fe), se();
      }
    }
  }
  function de(b) {
    we.call(this, n, b);
  }
  function h(b) {
    we.call(this, n, b);
  }
  function Fe(b) {
    we.call(this, n, b);
  }
  function Me(b) {
    we.call(this, n, b);
  }
  function me(b) {
    we.call(this, n, b);
  }
  function Pe(b) {
    we.call(this, n, b);
  }
  function Ze(b) {
    ct[b ? "unshift" : "push"](() => {
      S = b, t(10, S);
    });
  }
  function w() {
    L = this.textContent, C = this.innerHTML, t(11, L), t(9, C);
  }
  function $t(b) {
    ct[b ? "unshift" : "push"](() => {
      S = b, t(10, S);
    });
  }
  function el() {
    L = this.textContent, C = this.innerHTML, t(11, L), t(9, C);
  }
  return n.$$set = (b) => {
    "value" in b && t(17, i = b.value), "value_is_output" in b && t(18, o = b.value_is_output), "label" in b && t(0, s = b.label), "legend_label" in b && t(1, r = b.legend_label), "info" in b && t(2, f = b.info), "show_label" in b && t(3, a = b.show_label), "show_legend" in b && t(4, _ = b.show_legend), "show_legend_label" in b && t(5, u = b.show_legend_label), "container" in b && t(6, c = b.container), "color_map" in b && t(19, m = b.color_map), "show_copy_button" in b && t(7, p = b.show_copy_button), "disabled" in b && t(8, T = b.disabled);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*marked_el_text*/
    512 && W();
  }, z(), Q(), [
    s,
    r,
    f,
    a,
    _,
    u,
    c,
    p,
    T,
    C,
    S,
    L,
    M,
    g,
    se,
    O,
    E,
    i,
    o,
    m,
    de,
    h,
    Fe,
    Me,
    me,
    Pe,
    Ze,
    w,
    $t,
    el
  ];
}
class Yn extends Mn {
  constructor(e) {
    super(), Vn(
      this,
      e,
      Xn,
      Un,
      zn,
      {
        value: 17,
        value_is_output: 18,
        label: 0,
        legend_label: 1,
        info: 2,
        show_label: 3,
        show_legend: 4,
        show_legend_label: 5,
        container: 6,
        color_map: 19,
        show_copy_button: 7,
        disabled: 8
      },
      null,
      [-1, -1]
    );
  }
}
function pe(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
const {
  SvelteComponent: Gn,
  append: I,
  attr: q,
  component_subscribe: kt,
  detach: Jn,
  element: Kn,
  init: Qn,
  insert: xn,
  noop: vt,
  safe_not_equal: $n,
  set_style: Ne,
  svg_element: U,
  toggle_class: yt
} = window.__gradio__svelte__internal, { onMount: ei } = window.__gradio__svelte__internal;
function ti(n) {
  let e, t, l, i, o, s, r, f, a, _, u, c;
  return {
    c() {
      e = Kn("div"), t = U("svg"), l = U("g"), i = U("path"), o = U("path"), s = U("path"), r = U("path"), f = U("g"), a = U("path"), _ = U("path"), u = U("path"), c = U("path"), q(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), q(i, "fill", "#FF7C00"), q(i, "fill-opacity", "0.4"), q(i, "class", "svelte-43sxxs"), q(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), q(o, "fill", "#FF7C00"), q(o, "class", "svelte-43sxxs"), q(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), q(s, "fill", "#FF7C00"), q(s, "fill-opacity", "0.4"), q(s, "class", "svelte-43sxxs"), q(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), q(r, "fill", "#FF7C00"), q(r, "class", "svelte-43sxxs"), Ne(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), q(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), q(a, "fill", "#FF7C00"), q(a, "fill-opacity", "0.4"), q(a, "class", "svelte-43sxxs"), q(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), q(_, "fill", "#FF7C00"), q(_, "class", "svelte-43sxxs"), q(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), q(u, "fill", "#FF7C00"), q(u, "fill-opacity", "0.4"), q(u, "class", "svelte-43sxxs"), q(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), q(c, "fill", "#FF7C00"), q(c, "class", "svelte-43sxxs"), Ne(f, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), q(t, "viewBox", "-1200 -1200 3000 3000"), q(t, "fill", "none"), q(t, "xmlns", "http://www.w3.org/2000/svg"), q(t, "class", "svelte-43sxxs"), q(e, "class", "svelte-43sxxs"), yt(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(m, p) {
      xn(m, e, p), I(e, t), I(t, l), I(l, i), I(l, o), I(l, s), I(l, r), I(t, f), I(f, a), I(f, _), I(f, u), I(f, c);
    },
    p(m, [p]) {
      p & /*$top*/
      2 && Ne(l, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), p & /*$bottom*/
      4 && Ne(f, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), p & /*margin*/
      1 && yt(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: vt,
    o: vt,
    d(m) {
      m && Jn(e);
    }
  };
}
function li(n, e, t) {
  let l, i, { margin: o = !0 } = e;
  const s = _t([0, 0]);
  kt(n, s, (c) => t(1, l = c));
  const r = _t([0, 0]);
  kt(n, r, (c) => t(2, i = c));
  let f;
  async function a() {
    await Promise.all([s.set([125, 140]), r.set([-125, -140])]), await Promise.all([s.set([-125, 140]), r.set([125, -140])]), await Promise.all([s.set([-125, 0]), r.set([125, -0])]), await Promise.all([s.set([125, 0]), r.set([-125, 0])]);
  }
  async function _() {
    await a(), f || _();
  }
  async function u() {
    await Promise.all([s.set([125, 0]), r.set([-125, 0])]), _();
  }
  return ei(() => (u(), () => f = !0)), n.$$set = (c) => {
    "margin" in c && t(0, o = c.margin);
  }, [o, l, i, s, r];
}
class ni extends Gn {
  constructor(e) {
    super(), Qn(this, e, li, ti, $n, { margin: 0 });
  }
}
const {
  SvelteComponent: ii,
  append: _e,
  attr: Y,
  binding_callbacks: Ct,
  check_outros: Kt,
  create_component: oi,
  create_slot: si,
  destroy_component: fi,
  destroy_each: Qt,
  detach: k,
  element: $,
  empty: qe,
  ensure_array_like: Ee,
  get_all_dirty_from_scope: ri,
  get_slot_changes: ai,
  group_outros: xt,
  init: _i,
  insert: v,
  mount_component: ui,
  noop: Ue,
  safe_not_equal: ci,
  set_data: B,
  set_style: ie,
  space: G,
  text: F,
  toggle_class: Z,
  transition_in: ye,
  transition_out: Ce,
  update_slot_base: di
} = window.__gradio__svelte__internal, { tick: mi } = window.__gradio__svelte__internal, { onDestroy: bi } = window.__gradio__svelte__internal, gi = (n) => ({}), qt = (n) => ({});
function St(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l[40] = t, l;
}
function Lt(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l;
}
function hi(n) {
  let e, t = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, o;
  const s = (
    /*#slots*/
    n[29].error
  ), r = si(
    s,
    n,
    /*$$scope*/
    n[28],
    qt
  );
  return {
    c() {
      e = $("span"), l = F(t), i = G(), r && r.c(), Y(e, "class", "error svelte-1txqlrd");
    },
    m(f, a) {
      v(f, e, a), _e(e, l), v(f, i, a), r && r.m(f, a), o = !0;
    },
    p(f, a) {
      (!o || a[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      f[1]("common.error") + "") && B(l, t), r && r.p && (!o || a[0] & /*$$scope*/
      268435456) && di(
        r,
        s,
        f,
        /*$$scope*/
        f[28],
        o ? ai(
          s,
          /*$$scope*/
          f[28],
          a,
          gi
        ) : ri(
          /*$$scope*/
          f[28]
        ),
        qt
      );
    },
    i(f) {
      o || (ye(r, f), o = !0);
    },
    o(f) {
      Ce(r, f), o = !1;
    },
    d(f) {
      f && (k(e), k(i)), r && r.d(f);
    }
  };
}
function wi(n) {
  let e, t, l, i, o, s, r, f, a, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Tt(n)
  );
  function u(d, y) {
    if (
      /*progress*/
      d[7]
    )
      return vi;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return ki;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return pi;
  }
  let c = u(n), m = c && c(n), p = (
    /*timer*/
    n[5] && Nt(n)
  );
  const T = [Si, qi], S = [];
  function L(d, y) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = L(n)) && (s = S[o] = T[o](n));
  let C = !/*timer*/
  n[5] && Pt(n);
  return {
    c() {
      _ && _.c(), e = G(), t = $("div"), m && m.c(), l = G(), p && p.c(), i = G(), s && s.c(), r = G(), C && C.c(), f = qe(), Y(t, "class", "progress-text svelte-1txqlrd"), Z(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), Z(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(d, y) {
      _ && _.m(d, y), v(d, e, y), v(d, t, y), m && m.m(t, null), _e(t, l), p && p.m(t, null), v(d, i, y), ~o && S[o].m(d, y), v(d, r, y), C && C.m(d, y), v(d, f, y), a = !0;
    },
    p(d, y) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? _ ? _.p(d, y) : (_ = Tt(d), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), c === (c = u(d)) && m ? m.p(d, y) : (m && m.d(1), m = c && c(d), m && (m.c(), m.m(t, l))), /*timer*/
      d[5] ? p ? p.p(d, y) : (p = Nt(d), p.c(), p.m(t, null)) : p && (p.d(1), p = null), (!a || y[0] & /*variant*/
      256) && Z(
        t,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!a || y[0] & /*variant*/
      256) && Z(
        t,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let M = o;
      o = L(d), o === M ? ~o && S[o].p(d, y) : (s && (xt(), Ce(S[M], 1, 1, () => {
        S[M] = null;
      }), Kt()), ~o ? (s = S[o], s ? s.p(d, y) : (s = S[o] = T[o](d), s.c()), ye(s, 1), s.m(r.parentNode, r)) : s = null), /*timer*/
      d[5] ? C && (C.d(1), C = null) : C ? C.p(d, y) : (C = Pt(d), C.c(), C.m(f.parentNode, f));
    },
    i(d) {
      a || (ye(s), a = !0);
    },
    o(d) {
      Ce(s), a = !1;
    },
    d(d) {
      d && (k(e), k(t), k(i), k(r), k(f)), _ && _.d(d), m && m.d(), p && p.d(), ~o && S[o].d(d), C && C.d(d);
    }
  };
}
function Tt(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = $("div"), Y(e, "class", "eta-bar svelte-1txqlrd"), ie(e, "transform", t);
    },
    m(l, i) {
      v(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && ie(e, "transform", t);
    },
    d(l) {
      l && k(e);
    }
  };
}
function pi(n) {
  let e;
  return {
    c() {
      e = F("processing |");
    },
    m(t, l) {
      v(t, e, l);
    },
    p: Ue,
    d(t) {
      t && k(e);
    }
  };
}
function ki(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, o, s;
  return {
    c() {
      e = F("queue: "), l = F(t), i = F("/"), o = F(
        /*queue_size*/
        n[3]
      ), s = F(" |");
    },
    m(r, f) {
      v(r, e, f), v(r, l, f), v(r, i, f), v(r, o, f), v(r, s, f);
    },
    p(r, f) {
      f[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && B(l, t), f[0] & /*queue_size*/
      8 && B(
        o,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (k(e), k(l), k(i), k(o), k(s));
    }
  };
}
function vi(n) {
  let e, t = Ee(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Mt(Lt(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = qe();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      v(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = Ee(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = Lt(i, t, s);
          l[s] ? l[s].p(r, o) : (l[s] = Mt(r), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), Qt(l, i);
    }
  };
}
function Ft(n) {
  let e, t = (
    /*p*/
    n[38].unit + ""
  ), l, i, o = " ", s;
  function r(_, u) {
    return (
      /*p*/
      _[38].length != null ? Ci : yi
    );
  }
  let f = r(n), a = f(n);
  return {
    c() {
      a.c(), e = G(), l = F(t), i = F(" | "), s = F(o);
    },
    m(_, u) {
      a.m(_, u), v(_, e, u), v(_, l, u), v(_, i, u), v(_, s, u);
    },
    p(_, u) {
      f === (f = r(_)) && a ? a.p(_, u) : (a.d(1), a = f(_), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[38].unit + "") && B(l, t);
    },
    d(_) {
      _ && (k(e), k(l), k(i), k(s)), a.d(_);
    }
  };
}
function yi(n) {
  let e = pe(
    /*p*/
    n[38].index || 0
  ) + "", t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = pe(
        /*p*/
        l[38].index || 0
      ) + "") && B(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function Ci(n) {
  let e = pe(
    /*p*/
    n[38].index || 0
  ) + "", t, l, i = pe(
    /*p*/
    n[38].length
  ) + "", o;
  return {
    c() {
      t = F(e), l = F("/"), o = F(i);
    },
    m(s, r) {
      v(s, t, r), v(s, l, r), v(s, o, r);
    },
    p(s, r) {
      r[0] & /*progress*/
      128 && e !== (e = pe(
        /*p*/
        s[38].index || 0
      ) + "") && B(t, e), r[0] & /*progress*/
      128 && i !== (i = pe(
        /*p*/
        s[38].length
      ) + "") && B(o, i);
    },
    d(s) {
      s && (k(t), k(l), k(o));
    }
  };
}
function Mt(n) {
  let e, t = (
    /*p*/
    n[38].index != null && Ft(n)
  );
  return {
    c() {
      t && t.c(), e = qe();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].index != null ? t ? t.p(l, i) : (t = Ft(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function Nt(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = F(
        /*formatted_timer*/
        n[20]
      ), l = F(t), i = F("s");
    },
    m(o, s) {
      v(o, e, s), v(o, l, s), v(o, i, s);
    },
    p(o, s) {
      s[0] & /*formatted_timer*/
      1048576 && B(
        e,
        /*formatted_timer*/
        o[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && B(l, t);
    },
    d(o) {
      o && (k(e), k(l), k(i));
    }
  };
}
function qi(n) {
  let e, t;
  return e = new ni({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      oi(e.$$.fragment);
    },
    m(l, i) {
      ui(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      l[8] === "default"), e.$set(o);
    },
    i(l) {
      t || (ye(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Ce(e.$$.fragment, l), t = !1;
    },
    d(l) {
      fi(e, l);
    }
  };
}
function Si(n) {
  let e, t, l, i, o, s = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && Ht(n)
  );
  return {
    c() {
      e = $("div"), t = $("div"), r && r.c(), l = G(), i = $("div"), o = $("div"), Y(t, "class", "progress-level-inner svelte-1txqlrd"), Y(o, "class", "progress-bar svelte-1txqlrd"), ie(o, "width", s), Y(i, "class", "progress-bar-wrap svelte-1txqlrd"), Y(e, "class", "progress-level svelte-1txqlrd");
    },
    m(f, a) {
      v(f, e, a), _e(e, t), r && r.m(t, null), _e(e, l), _e(e, i), _e(i, o), n[30](o);
    },
    p(f, a) {
      /*progress*/
      f[7] != null ? r ? r.p(f, a) : (r = Ht(f), r.c(), r.m(t, null)) : r && (r.d(1), r = null), a[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      f[15] * 100}%`) && ie(o, "width", s);
    },
    i: Ue,
    o: Ue,
    d(f) {
      f && k(e), r && r.d(), n[30](null);
    }
  };
}
function Ht(n) {
  let e, t = Ee(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Et(St(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = qe();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      v(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = Ee(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = St(i, t, s);
          l[s] ? l[s].p(r, o) : (l[s] = Et(r), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), Qt(l, i);
    }
  };
}
function jt(n) {
  let e, t, l, i, o = (
    /*i*/
    n[40] !== 0 && Li()
  ), s = (
    /*p*/
    n[38].desc != null && Vt(n)
  ), r = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && At()
  ), f = (
    /*progress_level*/
    n[14] != null && zt(n)
  );
  return {
    c() {
      o && o.c(), e = G(), s && s.c(), t = G(), r && r.c(), l = G(), f && f.c(), i = qe();
    },
    m(a, _) {
      o && o.m(a, _), v(a, e, _), s && s.m(a, _), v(a, t, _), r && r.m(a, _), v(a, l, _), f && f.m(a, _), v(a, i, _);
    },
    p(a, _) {
      /*p*/
      a[38].desc != null ? s ? s.p(a, _) : (s = Vt(a), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      a[38].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[40]
      ] != null ? r || (r = At(), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null), /*progress_level*/
      a[14] != null ? f ? f.p(a, _) : (f = zt(a), f.c(), f.m(i.parentNode, i)) : f && (f.d(1), f = null);
    },
    d(a) {
      a && (k(e), k(t), k(l), k(i)), o && o.d(a), s && s.d(a), r && r.d(a), f && f.d(a);
    }
  };
}
function Li(n) {
  let e;
  return {
    c() {
      e = F(" /");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function Vt(n) {
  let e = (
    /*p*/
    n[38].desc + ""
  ), t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[38].desc + "") && B(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function At(n) {
  let e;
  return {
    c() {
      e = F("-");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function zt(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = F(e), l = F("%");
    },
    m(i, o) {
      v(i, t, o), v(i, l, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && B(t, e);
    },
    d(i) {
      i && (k(t), k(l));
    }
  };
}
function Et(n) {
  let e, t = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && jt(n)
  );
  return {
    c() {
      t && t.c(), e = qe();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? t ? t.p(l, i) : (t = jt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function Pt(n) {
  let e, t;
  return {
    c() {
      e = $("p"), t = F(
        /*loading_text*/
        n[9]
      ), Y(e, "class", "loading svelte-1txqlrd");
    },
    m(l, i) {
      v(l, e, i), _e(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && B(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && k(e);
    }
  };
}
function Ti(n) {
  let e, t, l, i, o;
  const s = [wi, hi], r = [];
  function f(a, _) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = f(n)) && (l = r[t] = s[t](n)), {
    c() {
      e = $("div"), l && l.c(), Y(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), Z(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), Z(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), Z(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), Z(
        e,
        "border",
        /*border*/
        n[12]
      ), ie(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), ie(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, _) {
      v(a, e, _), ~t && r[t].m(e, null), n[31](e), o = !0;
    },
    p(a, _) {
      let u = t;
      t = f(a), t === u ? ~t && r[t].p(a, _) : (l && (xt(), Ce(r[u], 1, 1, () => {
        r[u] = null;
      }), Kt()), ~t ? (l = r[t], l ? l.p(a, _) : (l = r[t] = s[t](a), l.c()), ye(l, 1), l.m(e, null)) : l = null), (!o || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-1txqlrd")) && Y(e, "class", i), (!o || _[0] & /*variant, show_progress, status, show_progress*/
      336) && Z(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!o || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Z(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!o || _[0] & /*variant, show_progress, status*/
      336) && Z(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!o || _[0] & /*variant, show_progress, border*/
      4416) && Z(
        e,
        "border",
        /*border*/
        a[12]
      ), _[0] & /*absolute*/
      1024 && ie(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && ie(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      o || (ye(l), o = !0);
    },
    o(a) {
      Ce(l), o = !1;
    },
    d(a) {
      a && k(e), ~t && r[t].d(), n[31](null);
    }
  };
}
let He = [], Oe = !1;
async function Fi(n, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (He.push(n), !Oe)
      Oe = !0;
    else
      return;
    await mi(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let l = 0; l < He.length; l++) {
        const o = He[l].getBoundingClientRect();
        (l === 0 || o.top + window.scrollY <= t[0]) && (t[0] = o.top + window.scrollY, t[1] = l);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Oe = !1, He = [];
    });
  }
}
function Mi(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e, { i18n: s } = e, { eta: r = null } = e, { queue_position: f } = e, { queue_size: a } = e, { status: _ } = e, { scroll_to_output: u = !1 } = e, { timer: c = !0 } = e, { show_progress: m = "full" } = e, { message: p = null } = e, { progress: T = null } = e, { variant: S = "default" } = e, { loading_text: L = "Loading..." } = e, { absolute: C = !0 } = e, { translucent: d = !1 } = e, { border: y = !1 } = e, { autoscroll: M } = e, g, R = !1, Q = 0, z = 0, D = null, W = null, se = 0, O = null, x, E = null, de = !0;
  const h = () => {
    t(0, r = t(26, D = t(19, me = null))), t(24, Q = performance.now()), t(25, z = 0), R = !0, Fe();
  };
  function Fe() {
    requestAnimationFrame(() => {
      t(25, z = (performance.now() - Q) / 1e3), R && Fe();
    });
  }
  function Me() {
    t(25, z = 0), t(0, r = t(26, D = t(19, me = null))), R && (R = !1);
  }
  bi(() => {
    R && Me();
  });
  let me = null;
  function Pe(w) {
    Ct[w ? "unshift" : "push"](() => {
      E = w, t(16, E), t(7, T), t(14, O), t(15, x);
    });
  }
  function Ze(w) {
    Ct[w ? "unshift" : "push"](() => {
      g = w, t(13, g);
    });
  }
  return n.$$set = (w) => {
    "i18n" in w && t(1, s = w.i18n), "eta" in w && t(0, r = w.eta), "queue_position" in w && t(2, f = w.queue_position), "queue_size" in w && t(3, a = w.queue_size), "status" in w && t(4, _ = w.status), "scroll_to_output" in w && t(21, u = w.scroll_to_output), "timer" in w && t(5, c = w.timer), "show_progress" in w && t(6, m = w.show_progress), "message" in w && t(22, p = w.message), "progress" in w && t(7, T = w.progress), "variant" in w && t(8, S = w.variant), "loading_text" in w && t(9, L = w.loading_text), "absolute" in w && t(10, C = w.absolute), "translucent" in w && t(11, d = w.translucent), "border" in w && t(12, y = w.border), "autoscroll" in w && t(23, M = w.autoscroll), "$$scope" in w && t(28, o = w.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (r === null && t(0, r = D), r != null && D !== r && (t(27, W = (performance.now() - Q) / 1e3 + r), t(19, me = W.toFixed(1)), t(26, D = r))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && t(17, se = W === null || W <= 0 || !z ? null : Math.min(z / W, 1)), n.$$.dirty[0] & /*progress*/
    128 && T != null && t(18, de = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (T != null ? t(14, O = T.map((w) => {
      if (w.index != null && w.length != null)
        return w.index / w.length;
      if (w.progress != null)
        return w.progress;
    })) : t(14, O = null), O ? (t(15, x = O[O.length - 1]), E && (x === 0 ? t(16, E.style.transition = "0", E) : t(16, E.style.transition = "150ms", E))) : t(15, x = void 0)), n.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? h() : Me()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && g && u && (_ === "pending" || _ === "complete") && Fi(g, M), n.$$.dirty[0] & /*status, message*/
    4194320, n.$$.dirty[0] & /*timer_diff*/
    33554432 && t(20, l = z.toFixed(1));
  }, [
    r,
    s,
    f,
    a,
    _,
    c,
    m,
    T,
    S,
    L,
    C,
    d,
    y,
    g,
    O,
    x,
    E,
    se,
    de,
    me,
    l,
    u,
    p,
    M,
    Q,
    z,
    D,
    W,
    o,
    i,
    Pe,
    Ze
  ];
}
class Ni extends ii {
  constructor(e) {
    super(), _i(
      this,
      e,
      Mi,
      Ti,
      ci,
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
const {
  SvelteComponent: Hi,
  add_flush_callback: Zt,
  assign: ji,
  bind: Bt,
  binding_callbacks: Rt,
  check_outros: Vi,
  create_component: Qe,
  destroy_component: xe,
  detach: Ai,
  flush: N,
  get_spread_object: zi,
  get_spread_update: Ei,
  group_outros: Pi,
  init: Zi,
  insert: Bi,
  mount_component: $e,
  safe_not_equal: Ri,
  space: Di,
  transition_in: ke,
  transition_out: Te
} = window.__gradio__svelte__internal;
function Dt(n) {
  let e, t;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[3].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[3].i18n
    ) },
    /*loading_status*/
    n[17]
  ];
  let i = {};
  for (let o = 0; o < l.length; o += 1)
    i = ji(i, l[o]);
  return e = new Ni({ props: i }), {
    c() {
      Qe(e.$$.fragment);
    },
    m(o, s) {
      $e(e, o, s), t = !0;
    },
    p(o, s) {
      const r = s & /*gradio, loading_status*/
      131080 ? Ei(l, [
        s & /*gradio*/
        8 && { autoscroll: (
          /*gradio*/
          o[3].autoscroll
        ) },
        s & /*gradio*/
        8 && { i18n: (
          /*gradio*/
          o[3].i18n
        ) },
        s & /*loading_status*/
        131072 && zi(
          /*loading_status*/
          o[17]
        )
      ]) : {};
      e.$set(r);
    },
    i(o) {
      t || (ke(e.$$.fragment, o), t = !0);
    },
    o(o) {
      Te(e.$$.fragment, o), t = !1;
    },
    d(o) {
      xe(e, o);
    }
  };
}
function Oi(n) {
  let e, t, l, i, o, s = (
    /*loading_status*/
    n[17] && Dt(n)
  );
  function r(_) {
    n[22](_);
  }
  function f(_) {
    n[23](_);
  }
  let a = {
    label: (
      /*label*/
      n[4]
    ),
    info: (
      /*info*/
      n[6]
    ),
    show_label: (
      /*show_label*/
      n[10]
    ),
    show_legend: (
      /*show_legend*/
      n[11]
    ),
    show_legend_label: (
      /*show_legend_label*/
      n[12]
    ),
    legend_label: (
      /*legend_label*/
      n[5]
    ),
    color_map: (
      /*color_map*/
      n[1]
    ),
    show_copy_button: (
      /*show_copy_button*/
      n[16]
    ),
    container: (
      /*container*/
      n[13]
    ),
    disabled: !/*interactive*/
    n[18]
  };
  return (
    /*value*/
    n[0] !== void 0 && (a.value = /*value*/
    n[0]), /*value_is_output*/
    n[2] !== void 0 && (a.value_is_output = /*value_is_output*/
    n[2]), t = new Yn({ props: a }), Rt.push(() => Bt(t, "value", r)), Rt.push(() => Bt(t, "value_is_output", f)), t.$on(
      "change",
      /*change_handler*/
      n[24]
    ), t.$on(
      "input",
      /*input_handler*/
      n[25]
    ), t.$on(
      "submit",
      /*submit_handler*/
      n[26]
    ), t.$on(
      "blur",
      /*blur_handler*/
      n[27]
    ), t.$on(
      "select",
      /*select_handler*/
      n[28]
    ), t.$on(
      "focus",
      /*focus_handler*/
      n[29]
    ), {
      c() {
        s && s.c(), e = Di(), Qe(t.$$.fragment);
      },
      m(_, u) {
        s && s.m(_, u), Bi(_, e, u), $e(t, _, u), o = !0;
      },
      p(_, u) {
        /*loading_status*/
        _[17] ? s ? (s.p(_, u), u & /*loading_status*/
        131072 && ke(s, 1)) : (s = Dt(_), s.c(), ke(s, 1), s.m(e.parentNode, e)) : s && (Pi(), Te(s, 1, 1, () => {
          s = null;
        }), Vi());
        const c = {};
        u & /*label*/
        16 && (c.label = /*label*/
        _[4]), u & /*info*/
        64 && (c.info = /*info*/
        _[6]), u & /*show_label*/
        1024 && (c.show_label = /*show_label*/
        _[10]), u & /*show_legend*/
        2048 && (c.show_legend = /*show_legend*/
        _[11]), u & /*show_legend_label*/
        4096 && (c.show_legend_label = /*show_legend_label*/
        _[12]), u & /*legend_label*/
        32 && (c.legend_label = /*legend_label*/
        _[5]), u & /*color_map*/
        2 && (c.color_map = /*color_map*/
        _[1]), u & /*show_copy_button*/
        65536 && (c.show_copy_button = /*show_copy_button*/
        _[16]), u & /*container*/
        8192 && (c.container = /*container*/
        _[13]), u & /*interactive*/
        262144 && (c.disabled = !/*interactive*/
        _[18]), !l && u & /*value*/
        1 && (l = !0, c.value = /*value*/
        _[0], Zt(() => l = !1)), !i && u & /*value_is_output*/
        4 && (i = !0, c.value_is_output = /*value_is_output*/
        _[2], Zt(() => i = !1)), t.$set(c);
      },
      i(_) {
        o || (ke(s), ke(t.$$.fragment, _), o = !0);
      },
      o(_) {
        Te(s), Te(t.$$.fragment, _), o = !1;
      },
      d(_) {
        _ && Ai(e), s && s.d(_), xe(t, _);
      }
    }
  );
}
function Ii(n) {
  let e, t;
  return e = new wl({
    props: {
      visible: (
        /*visible*/
        n[9]
      ),
      elem_id: (
        /*elem_id*/
        n[7]
      ),
      elem_classes: (
        /*elem_classes*/
        n[8]
      ),
      scale: (
        /*scale*/
        n[14]
      ),
      min_width: (
        /*min_width*/
        n[15]
      ),
      allow_overflow: !1,
      padding: (
        /*container*/
        n[13]
      ),
      $$slots: { default: [Oi] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Qe(e.$$.fragment);
    },
    m(l, i) {
      $e(e, l, i), t = !0;
    },
    p(l, [i]) {
      const o = {};
      i & /*visible*/
      512 && (o.visible = /*visible*/
      l[9]), i & /*elem_id*/
      128 && (o.elem_id = /*elem_id*/
      l[7]), i & /*elem_classes*/
      256 && (o.elem_classes = /*elem_classes*/
      l[8]), i & /*scale*/
      16384 && (o.scale = /*scale*/
      l[14]), i & /*min_width*/
      32768 && (o.min_width = /*min_width*/
      l[15]), i & /*container*/
      8192 && (o.padding = /*container*/
      l[13]), i & /*$$scope, label, info, show_label, show_legend, show_legend_label, legend_label, color_map, show_copy_button, container, interactive, value, value_is_output, gradio, loading_status*/
      1074216063 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (ke(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Te(e.$$.fragment, l), t = !1;
    },
    d(l) {
      xe(e, l);
    }
  };
}
function Ui(n, e, t) {
  let { gradio: l } = e, { label: i = "Highlighted Textbox" } = e, { legend_label: o = "Highlights:" } = e, { info: s = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: f = [] } = e, { visible: a = !0 } = e, { value: _ } = e, { show_label: u } = e, { show_legend: c } = e, { show_legend_label: m } = e, { color_map: p = {} } = e, { container: T = !0 } = e, { scale: S = null } = e, { min_width: L = void 0 } = e, { show_copy_button: C = !1 } = e, { loading_status: d = void 0 } = e, { value_is_output: y = !1 } = e, { combine_adjacent: M = !1 } = e, { interactive: g = !0 } = e;
  const R = !1, Q = !0;
  function z(h) {
    _ = h, t(0, _), t(19, M);
  }
  function D(h) {
    y = h, t(2, y);
  }
  const W = () => l.dispatch("change"), se = () => l.dispatch("input"), O = () => l.dispatch("submit"), x = () => l.dispatch("blur"), E = (h) => l.dispatch("select", h.detail), de = () => l.dispatch("focus");
  return n.$$set = (h) => {
    "gradio" in h && t(3, l = h.gradio), "label" in h && t(4, i = h.label), "legend_label" in h && t(5, o = h.legend_label), "info" in h && t(6, s = h.info), "elem_id" in h && t(7, r = h.elem_id), "elem_classes" in h && t(8, f = h.elem_classes), "visible" in h && t(9, a = h.visible), "value" in h && t(0, _ = h.value), "show_label" in h && t(10, u = h.show_label), "show_legend" in h && t(11, c = h.show_legend), "show_legend_label" in h && t(12, m = h.show_legend_label), "color_map" in h && t(1, p = h.color_map), "container" in h && t(13, T = h.container), "scale" in h && t(14, S = h.scale), "min_width" in h && t(15, L = h.min_width), "show_copy_button" in h && t(16, C = h.show_copy_button), "loading_status" in h && t(17, d = h.loading_status), "value_is_output" in h && t(2, y = h.value_is_output), "combine_adjacent" in h && t(19, M = h.combine_adjacent), "interactive" in h && t(18, g = h.interactive);
  }, n.$$.update = () => {
    n.$$.dirty & /*color_map*/
    2 && !p && Object.keys(p).length && t(1, p), n.$$.dirty & /*value, combine_adjacent*/
    524289 && _ && M && t(0, _ = Ln(_, "equal"));
  }, [
    _,
    p,
    y,
    l,
    i,
    o,
    s,
    r,
    f,
    a,
    u,
    c,
    m,
    T,
    S,
    L,
    C,
    d,
    g,
    M,
    R,
    Q,
    z,
    D,
    W,
    se,
    O,
    x,
    E,
    de
  ];
}
class Xi extends Hi {
  constructor(e) {
    super(), Zi(this, e, Ui, Ii, Ri, {
      gradio: 3,
      label: 4,
      legend_label: 5,
      info: 6,
      elem_id: 7,
      elem_classes: 8,
      visible: 9,
      value: 0,
      show_label: 10,
      show_legend: 11,
      show_legend_label: 12,
      color_map: 1,
      container: 13,
      scale: 14,
      min_width: 15,
      show_copy_button: 16,
      loading_status: 17,
      value_is_output: 2,
      combine_adjacent: 19,
      interactive: 18,
      autofocus: 20,
      autoscroll: 21
    });
  }
  get gradio() {
    return this.$$.ctx[3];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), N();
  }
  get label() {
    return this.$$.ctx[4];
  }
  set label(e) {
    this.$$set({ label: e }), N();
  }
  get legend_label() {
    return this.$$.ctx[5];
  }
  set legend_label(e) {
    this.$$set({ legend_label: e }), N();
  }
  get info() {
    return this.$$.ctx[6];
  }
  set info(e) {
    this.$$set({ info: e }), N();
  }
  get elem_id() {
    return this.$$.ctx[7];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), N();
  }
  get elem_classes() {
    return this.$$.ctx[8];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), N();
  }
  get visible() {
    return this.$$.ctx[9];
  }
  set visible(e) {
    this.$$set({ visible: e }), N();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), N();
  }
  get show_label() {
    return this.$$.ctx[10];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), N();
  }
  get show_legend() {
    return this.$$.ctx[11];
  }
  set show_legend(e) {
    this.$$set({ show_legend: e }), N();
  }
  get show_legend_label() {
    return this.$$.ctx[12];
  }
  set show_legend_label(e) {
    this.$$set({ show_legend_label: e }), N();
  }
  get color_map() {
    return this.$$.ctx[1];
  }
  set color_map(e) {
    this.$$set({ color_map: e }), N();
  }
  get container() {
    return this.$$.ctx[13];
  }
  set container(e) {
    this.$$set({ container: e }), N();
  }
  get scale() {
    return this.$$.ctx[14];
  }
  set scale(e) {
    this.$$set({ scale: e }), N();
  }
  get min_width() {
    return this.$$.ctx[15];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), N();
  }
  get show_copy_button() {
    return this.$$.ctx[16];
  }
  set show_copy_button(e) {
    this.$$set({ show_copy_button: e }), N();
  }
  get loading_status() {
    return this.$$.ctx[17];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), N();
  }
  get value_is_output() {
    return this.$$.ctx[2];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), N();
  }
  get combine_adjacent() {
    return this.$$.ctx[19];
  }
  set combine_adjacent(e) {
    this.$$set({ combine_adjacent: e }), N();
  }
  get interactive() {
    return this.$$.ctx[18];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), N();
  }
  get autofocus() {
    return this.$$.ctx[20];
  }
  get autoscroll() {
    return this.$$.ctx[21];
  }
}
export {
  Xi as default
};
