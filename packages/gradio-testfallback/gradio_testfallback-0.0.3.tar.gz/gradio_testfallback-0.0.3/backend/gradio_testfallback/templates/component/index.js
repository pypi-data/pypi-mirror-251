const {
  SvelteComponent: Ct,
  append: A,
  attr: F,
  check_outros: je,
  create_component: zt,
  destroy_component: Ft,
  destroy_each: Lt,
  detach: L,
  element: M,
  empty: de,
  ensure_array_like: Me,
  group_outros: Ce,
  init: St,
  insert: S,
  listen: te,
  mount_component: Vt,
  noop: fe,
  run_all: ct,
  safe_not_equal: Nt,
  set_data: R,
  space: he,
  text: E,
  toggle_class: X,
  transition_in: G,
  transition_out: W
} = window.__gradio__svelte__internal;
function Be(n, e, t) {
  const l = n.slice();
  return l[10] = e[t], l[12] = t, l;
}
function At(n) {
  let e, t = (
    /*brackets*/
    n[6][0] + ""
  ), l, i, f, s, o, r = (
    /*brackets*/
    n[6][1] + ""
  ), _, a, d, c, m, h = Me(
    /*items*/
    n[5]
  ), v = [];
  for (let b = 0; b < h.length; b += 1)
    v[b] = Ze(Be(n, h, b));
  const z = (b) => W(v[b], 1, 1, () => {
    v[b] = null;
  });
  let j = !/*_last*/
  n[3] && Ee();
  return {
    c() {
      e = M("span"), l = E(t), i = he(), f = M("ul");
      for (let b = 0; b < v.length; b += 1)
        v[b].c();
      s = he(), o = M("span"), _ = E(r), j && j.c(), a = de(), F(e, "class", "_jsonBkt svelte-6z96o6"), F(e, "role", "button"), F(e, "tabindex", "0"), X(
        e,
        "isArray",
        /*isArray*/
        n[4]
      ), F(f, "class", "_jsonList svelte-6z96o6"), F(o, "class", "_jsonBkt svelte-6z96o6"), F(o, "role", "button"), F(o, "tabindex", "0"), X(
        o,
        "isArray",
        /*isArray*/
        n[4]
      );
    },
    m(b, u) {
      S(b, e, u), A(e, l), S(b, i, u), S(b, f, u);
      for (let g = 0; g < v.length; g += 1)
        v[g] && v[g].m(f, null);
      S(b, s, u), S(b, o, u), A(o, _), j && j.m(b, u), S(b, a, u), d = !0, c || (m = [
        te(
          e,
          "click",
          /*clicked*/
          n[8]
        ),
        te(
          e,
          "keydown",
          /*pressed*/
          n[9]
        ),
        te(
          o,
          "click",
          /*clicked*/
          n[8]
        ),
        te(
          o,
          "keydown",
          /*pressed*/
          n[9]
        )
      ], c = !0);
    },
    p(b, u) {
      if ((!d || u & /*brackets*/
      64) && t !== (t = /*brackets*/
      b[6][0] + "") && R(l, t), (!d || u & /*isArray*/
      16) && X(
        e,
        "isArray",
        /*isArray*/
        b[4]
      ), u & /*json, items, depth, _cur, getType, format, isArray*/
      55) {
        h = Me(
          /*items*/
          b[5]
        );
        let g;
        for (g = 0; g < h.length; g += 1) {
          const V = Be(b, h, g);
          v[g] ? (v[g].p(V, u), G(v[g], 1)) : (v[g] = Ze(V), v[g].c(), G(v[g], 1), v[g].m(f, null));
        }
        for (Ce(), g = h.length; g < v.length; g += 1)
          z(g);
        je();
      }
      (!d || u & /*brackets*/
      64) && r !== (r = /*brackets*/
      b[6][1] + "") && R(_, r), (!d || u & /*isArray*/
      16) && X(
        o,
        "isArray",
        /*isArray*/
        b[4]
      ), /*_last*/
      b[3] ? j && (j.d(1), j = null) : j || (j = Ee(), j.c(), j.m(a.parentNode, a));
    },
    i(b) {
      if (!d) {
        for (let u = 0; u < h.length; u += 1)
          G(v[u]);
        d = !0;
      }
    },
    o(b) {
      v = v.filter(Boolean);
      for (let u = 0; u < v.length; u += 1)
        W(v[u]);
      d = !1;
    },
    d(b) {
      b && (L(e), L(i), L(f), L(s), L(o), L(a)), Lt(v, b), j && j.d(b), c = !1, ct(m);
    }
  };
}
function Mt(n) {
  let e, t = (
    /*brackets*/
    n[6][0] + ""
  ), l, i, f = (
    /*brackets*/
    n[6][1] + ""
  ), s, o, r, _, a = !/*_last*/
  n[3] && /*collapsed*/
  n[7] && De();
  return {
    c() {
      e = M("span"), l = E(t), i = E("..."), s = E(f), a && a.c(), o = de(), F(e, "class", "_jsonBkt svelte-6z96o6"), F(e, "role", "button"), F(e, "tabindex", "0"), X(
        e,
        "isArray",
        /*isArray*/
        n[4]
      );
    },
    m(d, c) {
      S(d, e, c), A(e, l), A(e, i), A(e, s), a && a.m(d, c), S(d, o, c), r || (_ = [
        te(
          e,
          "click",
          /*clicked*/
          n[8]
        ),
        te(
          e,
          "keydown",
          /*pressed*/
          n[9]
        )
      ], r = !0);
    },
    p(d, c) {
      c & /*brackets*/
      64 && t !== (t = /*brackets*/
      d[6][0] + "") && R(l, t), c & /*brackets*/
      64 && f !== (f = /*brackets*/
      d[6][1] + "") && R(s, f), c & /*isArray*/
      16 && X(
        e,
        "isArray",
        /*isArray*/
        d[4]
      ), !/*_last*/
      d[3] && /*collapsed*/
      d[7] ? a || (a = De(), a.c(), a.m(o.parentNode, o)) : a && (a.d(1), a = null);
    },
    i: fe,
    o: fe,
    d(d) {
      d && (L(e), L(o)), a && a.d(d), r = !1, ct(_);
    }
  };
}
function Bt(n) {
  let e, t = (
    /*brackets*/
    n[6][0] + ""
  ), l, i = (
    /*brackets*/
    n[6][1] + ""
  ), f, s, o = !/*_last*/
  n[3] && Ie();
  return {
    c() {
      e = M("span"), l = E(t), f = E(i), o && o.c(), s = de(), F(e, "class", "_jsonBkt empty svelte-6z96o6"), X(
        e,
        "isArray",
        /*isArray*/
        n[4]
      );
    },
    m(r, _) {
      S(r, e, _), A(e, l), A(e, f), o && o.m(r, _), S(r, s, _);
    },
    p(r, _) {
      _ & /*brackets*/
      64 && t !== (t = /*brackets*/
      r[6][0] + "") && R(l, t), _ & /*brackets*/
      64 && i !== (i = /*brackets*/
      r[6][1] + "") && R(f, i), _ & /*isArray*/
      16 && X(
        e,
        "isArray",
        /*isArray*/
        r[4]
      ), /*_last*/
      r[3] ? o && (o.d(1), o = null) : o || (o = Ie(), o.c(), o.m(s.parentNode, s));
    },
    i: fe,
    o: fe,
    d(r) {
      r && (L(e), L(s)), o && o.d(r);
    }
  };
}
function Pe(n) {
  let e, t, l = (
    /*i*/
    n[10] + ""
  ), i, f, s;
  return {
    c() {
      e = M("span"), t = E('"'), i = E(l), f = E('"'), s = M("span"), s.textContent = ":", F(e, "class", "_jsonKey svelte-6z96o6"), F(s, "class", "_jsonSep svelte-6z96o6");
    },
    m(o, r) {
      S(o, e, r), A(e, t), A(e, i), A(e, f), S(o, s, r);
    },
    p(o, r) {
      r & /*items*/
      32 && l !== (l = /*i*/
      o[10] + "") && R(i, l);
    },
    d(o) {
      o && (L(e), L(s));
    }
  };
}
function Pt(n) {
  let e, t = Je(
    /*json*/
    n[0][
      /*i*/
      n[10]
    ]
  ) + "", l, i, f, s = (
    /*idx*/
    n[12] < /*items*/
    n[5].length - 1 && Te()
  );
  return {
    c() {
      e = M("span"), l = E(t), s && s.c(), f = de(), F(e, "class", i = "_jsonVal " + ce(
        /*json*/
        n[0][
          /*i*/
          n[10]
        ]
      ) + " svelte-6z96o6");
    },
    m(o, r) {
      S(o, e, r), A(e, l), s && s.m(o, r), S(o, f, r);
    },
    p(o, r) {
      r & /*json, items*/
      33 && t !== (t = Je(
        /*json*/
        o[0][
          /*i*/
          o[10]
        ]
      ) + "") && R(l, t), r & /*json, items*/
      33 && i !== (i = "_jsonVal " + ce(
        /*json*/
        o[0][
          /*i*/
          o[10]
        ]
      ) + " svelte-6z96o6") && F(e, "class", i), /*idx*/
      o[12] < /*items*/
      o[5].length - 1 ? s || (s = Te(), s.c(), s.m(f.parentNode, f)) : s && (s.d(1), s = null);
    },
    i: fe,
    o: fe,
    d(o) {
      o && (L(e), L(f)), s && s.d(o);
    }
  };
}
function Tt(n) {
  let e, t;
  return e = new dt({
    props: {
      json: (
        /*json*/
        n[0][
          /*i*/
          n[10]
        ]
      ),
      depth: (
        /*depth*/
        n[1]
      ),
      _cur: (
        /*_cur*/
        n[2] + 1
      ),
      _last: (
        /*idx*/
        n[12] === /*items*/
        n[5].length - 1
      )
    }
  }), {
    c() {
      zt(e.$$.fragment);
    },
    m(l, i) {
      Vt(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i & /*json, items*/
      33 && (f.json = /*json*/
      l[0][
        /*i*/
        l[10]
      ]), i & /*depth*/
      2 && (f.depth = /*depth*/
      l[1]), i & /*_cur*/
      4 && (f._cur = /*_cur*/
      l[2] + 1), i & /*items*/
      32 && (f._last = /*idx*/
      l[12] === /*items*/
      l[5].length - 1), e.$set(f);
    },
    i(l) {
      t || (G(e.$$.fragment, l), t = !0);
    },
    o(l) {
      W(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ft(e, l);
    }
  };
}
function Te(n) {
  let e;
  return {
    c() {
      e = M("span"), e.textContent = ",", F(e, "class", "_jsonSep svelte-6z96o6");
    },
    m(t, l) {
      S(t, e, l);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Ze(n) {
  let e, t, l, i, f, s, o, r = !/*isArray*/
  n[4] && Pe(n);
  const _ = [Tt, Pt], a = [];
  function d(c, m) {
    return m & /*json, items*/
    33 && (l = null), l == null && (l = ce(
      /*json*/
      c[0][
        /*i*/
        c[10]
      ]
    ) === "object"), l ? 0 : 1;
  }
  return i = d(n, -1), f = a[i] = _[i](n), {
    c() {
      e = M("li"), r && r.c(), t = he(), f.c(), s = he(), F(e, "class", "svelte-6z96o6");
    },
    m(c, m) {
      S(c, e, m), r && r.m(e, null), A(e, t), a[i].m(e, null), A(e, s), o = !0;
    },
    p(c, m) {
      /*isArray*/
      c[4] ? r && (r.d(1), r = null) : r ? r.p(c, m) : (r = Pe(c), r.c(), r.m(e, t));
      let h = i;
      i = d(c, m), i === h ? a[i].p(c, m) : (Ce(), W(a[h], 1, 1, () => {
        a[h] = null;
      }), je(), f = a[i], f ? f.p(c, m) : (f = a[i] = _[i](c), f.c()), G(f, 1), f.m(e, s));
    },
    i(c) {
      o || (G(f), o = !0);
    },
    o(c) {
      W(f), o = !1;
    },
    d(c) {
      c && L(e), r && r.d(), a[i].d();
    }
  };
}
function Ee(n) {
  let e;
  return {
    c() {
      e = M("span"), e.textContent = ",", F(e, "class", "_jsonSep svelte-6z96o6");
    },
    m(t, l) {
      S(t, e, l);
    },
    d(t) {
      t && L(e);
    }
  };
}
function De(n) {
  let e;
  return {
    c() {
      e = M("span"), e.textContent = ",", F(e, "class", "_jsonSep svelte-6z96o6");
    },
    m(t, l) {
      S(t, e, l);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Ie(n) {
  let e;
  return {
    c() {
      e = M("span"), e.textContent = ",", F(e, "class", "_jsonSep svelte-6z96o6");
    },
    m(t, l) {
      S(t, e, l);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Zt(n) {
  let e, t, l, i;
  const f = [Bt, Mt, At], s = [];
  function o(r, _) {
    return (
      /*items*/
      r[5].length ? (
        /*collapsed*/
        r[7] ? 1 : 2
      ) : 0
    );
  }
  return e = o(n), t = s[e] = f[e](n), {
    c() {
      t.c(), l = de();
    },
    m(r, _) {
      s[e].m(r, _), S(r, l, _), i = !0;
    },
    p(r, [_]) {
      let a = e;
      e = o(r), e === a ? s[e].p(r, _) : (Ce(), W(s[a], 1, 1, () => {
        s[a] = null;
      }), je(), t = s[e], t ? t.p(r, _) : (t = s[e] = f[e](r), t.c()), G(t, 1), t.m(l.parentNode, l));
    },
    i(r) {
      i || (G(t), i = !0);
    },
    o(r) {
      W(t), i = !1;
    },
    d(r) {
      r && L(l), s[e].d(r);
    }
  };
}
function ce(n) {
  return n === null ? "null" : typeof n;
}
function Je(n) {
  const e = ce(n);
  return e === "string" ? `"${n}"` : e === "function" ? "f () {...}" : e === "symbol" ? n.toString() : n;
}
function Et(n, e, t) {
  let { json: l } = e, { depth: i = 1 / 0 } = e, { _cur: f = 0 } = e, { _last: s = !0 } = e, o, r = !1, _ = ["", ""], a = !1;
  function d() {
    t(7, a = !a);
  }
  function c(m) {
    m instanceof KeyboardEvent && ["Enter", " "].includes(m.key) && d();
  }
  return n.$$set = (m) => {
    "json" in m && t(0, l = m.json), "depth" in m && t(1, i = m.depth), "_cur" in m && t(2, f = m._cur), "_last" in m && t(3, s = m._last);
  }, n.$$.update = () => {
    n.$$.dirty & /*json, isArray*/
    17 && (t(5, o = ce(l) === "object" ? Object.keys(l) : []), t(4, r = Array.isArray(l)), t(6, _ = r ? ["[", "]"] : ["{", "}"])), n.$$.dirty & /*depth, _cur*/
    6 && t(7, a = i < f);
  }, [
    l,
    i,
    f,
    s,
    r,
    o,
    _,
    a,
    d,
    c
  ];
}
class dt extends Ct {
  constructor(e) {
    super(), St(this, e, Et, Zt, Nt, { json: 0, depth: 1, _cur: 2, _last: 3 });
  }
}
const {
  SvelteComponent: Dt,
  assign: It,
  create_slot: Jt,
  detach: Kt,
  element: Ot,
  get_all_dirty_from_scope: Xt,
  get_slot_changes: Yt,
  get_spread_update: Gt,
  init: Rt,
  insert: Ut,
  safe_not_equal: Ht,
  set_dynamic_element_data: Ke,
  set_style: N,
  toggle_class: O,
  transition_in: mt,
  transition_out: bt,
  update_slot_base: Qt
} = window.__gradio__svelte__internal;
function Wt(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), f = Jt(
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
  ], o = {};
  for (let r = 0; r < s.length; r += 1)
    o = It(o, s[r]);
  return {
    c() {
      e = Ot(
        /*tag*/
        n[14]
      ), f && f.c(), Ke(
        /*tag*/
        n[14]
      )(e, o), O(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), O(
        e,
        "padded",
        /*padding*/
        n[6]
      ), O(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), O(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), N(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), N(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), N(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), N(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), N(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), N(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), N(e, "border-width", "var(--block-border-width)");
    },
    m(r, _) {
      Ut(r, e, _), f && f.m(e, null), l = !0;
    },
    p(r, _) {
      f && f.p && (!l || _ & /*$$scope*/
      131072) && Qt(
        f,
        i,
        r,
        /*$$scope*/
        r[17],
        l ? Yt(
          i,
          /*$$scope*/
          r[17],
          _,
          null
        ) : Xt(
          /*$$scope*/
          r[17]
        ),
        null
      ), Ke(
        /*tag*/
        r[14]
      )(e, o = Gt(s, [
        (!l || _ & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          r[7]
        ) },
        (!l || _ & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          r[2]
        ) },
        (!l || _ & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        r[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), O(
        e,
        "hidden",
        /*visible*/
        r[10] === !1
      ), O(
        e,
        "padded",
        /*padding*/
        r[6]
      ), O(
        e,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), O(e, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), _ & /*height*/
      1 && N(
        e,
        "height",
        /*get_dimension*/
        r[15](
          /*height*/
          r[0]
        )
      ), _ & /*width*/
      2 && N(e, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : (
        /*get_dimension*/
        r[15](
          /*width*/
          r[1]
        )
      )), _ & /*variant*/
      16 && N(
        e,
        "border-style",
        /*variant*/
        r[4]
      ), _ & /*allow_overflow*/
      2048 && N(
        e,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), _ & /*scale*/
      4096 && N(
        e,
        "flex-grow",
        /*scale*/
        r[12]
      ), _ & /*min_width*/
      8192 && N(e, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      l || (mt(f, r), l = !0);
    },
    o(r) {
      bt(f, r), l = !1;
    },
    d(r) {
      r && Kt(e), f && f.d(r);
    }
  };
}
function xt(n) {
  let e, t = (
    /*tag*/
    n[14] && Wt(n)
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
      e || (mt(t, l), e = !0);
    },
    o(l) {
      bt(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function $t(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: s = void 0 } = e, { elem_id: o = "" } = e, { elem_classes: r = [] } = e, { variant: _ = "solid" } = e, { border_mode: a = "base" } = e, { padding: d = !0 } = e, { type: c = "normal" } = e, { test_id: m = void 0 } = e, { explicit_call: h = !1 } = e, { container: v = !0 } = e, { visible: z = !0 } = e, { allow_overflow: j = !0 } = e, { scale: b = null } = e, { min_width: u = 0 } = e, g = c === "fieldset" ? "fieldset" : "div";
  const V = (k) => {
    if (k !== void 0) {
      if (typeof k == "number")
        return k + "px";
      if (typeof k == "string")
        return k;
    }
  };
  return n.$$set = (k) => {
    "height" in k && t(0, f = k.height), "width" in k && t(1, s = k.width), "elem_id" in k && t(2, o = k.elem_id), "elem_classes" in k && t(3, r = k.elem_classes), "variant" in k && t(4, _ = k.variant), "border_mode" in k && t(5, a = k.border_mode), "padding" in k && t(6, d = k.padding), "type" in k && t(16, c = k.type), "test_id" in k && t(7, m = k.test_id), "explicit_call" in k && t(8, h = k.explicit_call), "container" in k && t(9, v = k.container), "visible" in k && t(10, z = k.visible), "allow_overflow" in k && t(11, j = k.allow_overflow), "scale" in k && t(12, b = k.scale), "min_width" in k && t(13, u = k.min_width), "$$scope" in k && t(17, i = k.$$scope);
  }, [
    f,
    s,
    o,
    r,
    _,
    a,
    d,
    m,
    h,
    v,
    z,
    j,
    b,
    u,
    g,
    V,
    c,
    i,
    l
  ];
}
class el extends Dt {
  constructor(e) {
    super(), Rt(this, e, $t, xt, Ht, {
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
const tl = [
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
], Oe = {
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
tl.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: Oe[e][t],
      secondary: Oe[e][l]
    }
  }),
  {}
);
function le(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function ke() {
}
function ll(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const gt = typeof window < "u";
let Xe = gt ? () => window.performance.now() : () => Date.now(), pt = gt ? (n) => requestAnimationFrame(n) : ke;
const ie = /* @__PURE__ */ new Set();
function kt(n) {
  ie.forEach((e) => {
    e.c(n) || (ie.delete(e), e.f());
  }), ie.size !== 0 && pt(kt);
}
function nl(n) {
  let e;
  return ie.size === 0 && pt(kt), {
    promise: new Promise((t) => {
      ie.add(e = { c: n, f: t });
    }),
    abort() {
      ie.delete(e);
    }
  };
}
const ee = [];
function il(n, e = ke) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(o) {
    if (ll(n, o) && (n = o, t)) {
      const r = !ee.length;
      for (const _ of l)
        _[1](), ee.push(_, n);
      if (r) {
        for (let _ = 0; _ < ee.length; _ += 2)
          ee[_][0](ee[_ + 1]);
        ee.length = 0;
      }
    }
  }
  function f(o) {
    i(o(n));
  }
  function s(o, r = ke) {
    const _ = [o, r];
    return l.add(_), l.size === 1 && (t = e(i, f) || ke), o(n), () => {
      l.delete(_), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: s };
}
function Ye(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function ve(n, e, t, l) {
  if (typeof t == "number" || Ye(t)) {
    const i = l - t, f = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, o = n.opts.damping * f, r = (s - o) * n.inv_mass, _ = (f + r) * n.dt;
    return Math.abs(_) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Ye(t) ? new Date(t.getTime() + _) : t + _);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => ve(n, e[f], t[f], l[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = ve(n, e[f], t[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Ge(n, e = {}) {
  const t = il(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let s, o, r, _ = n, a = n, d = 1, c = 0, m = !1;
  function h(z, j = {}) {
    a = z;
    const b = r = {};
    return n == null || j.hard || v.stiffness >= 1 && v.damping >= 1 ? (m = !0, s = Xe(), _ = z, t.set(n = a), Promise.resolve()) : (j.soft && (c = 1 / ((j.soft === !0 ? 0.5 : +j.soft) * 60), d = 0), o || (s = Xe(), m = !1, o = nl((u) => {
      if (m)
        return m = !1, o = null, !1;
      d = Math.min(d + c, 1);
      const g = {
        inv_mass: d,
        opts: v,
        settled: !0,
        dt: (u - s) * 60 / 1e3
      }, V = ve(g, _, n, a);
      return s = u, _ = n, t.set(n = V), g.settled && (o = null), !g.settled;
    })), new Promise((u) => {
      o.promise.then(() => {
        b === r && u();
      });
    }));
  }
  const v = {
    set: h,
    update: (z, j) => h(z(a, n), j),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return v;
}
const {
  SvelteComponent: fl,
  append: T,
  attr: q,
  component_subscribe: Re,
  detach: sl,
  element: ol,
  init: rl,
  insert: _l,
  noop: Ue,
  safe_not_equal: al,
  set_style: ge,
  svg_element: Z,
  toggle_class: He
} = window.__gradio__svelte__internal, { onMount: ul } = window.__gradio__svelte__internal;
function cl(n) {
  let e, t, l, i, f, s, o, r, _, a, d, c;
  return {
    c() {
      e = ol("div"), t = Z("svg"), l = Z("g"), i = Z("path"), f = Z("path"), s = Z("path"), o = Z("path"), r = Z("g"), _ = Z("path"), a = Z("path"), d = Z("path"), c = Z("path"), q(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), q(i, "fill", "#FF7C00"), q(i, "fill-opacity", "0.4"), q(i, "class", "svelte-43sxxs"), q(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), q(f, "fill", "#FF7C00"), q(f, "class", "svelte-43sxxs"), q(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), q(s, "fill", "#FF7C00"), q(s, "fill-opacity", "0.4"), q(s, "class", "svelte-43sxxs"), q(o, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), q(o, "fill", "#FF7C00"), q(o, "class", "svelte-43sxxs"), ge(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), q(_, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), q(_, "fill", "#FF7C00"), q(_, "fill-opacity", "0.4"), q(_, "class", "svelte-43sxxs"), q(a, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), q(a, "fill", "#FF7C00"), q(a, "class", "svelte-43sxxs"), q(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), q(d, "fill", "#FF7C00"), q(d, "fill-opacity", "0.4"), q(d, "class", "svelte-43sxxs"), q(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), q(c, "fill", "#FF7C00"), q(c, "class", "svelte-43sxxs"), ge(r, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), q(t, "viewBox", "-1200 -1200 3000 3000"), q(t, "fill", "none"), q(t, "xmlns", "http://www.w3.org/2000/svg"), q(t, "class", "svelte-43sxxs"), q(e, "class", "svelte-43sxxs"), He(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(m, h) {
      _l(m, e, h), T(e, t), T(t, l), T(l, i), T(l, f), T(l, s), T(l, o), T(t, r), T(r, _), T(r, a), T(r, d), T(r, c);
    },
    p(m, [h]) {
      h & /*$top*/
      2 && ge(l, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), h & /*$bottom*/
      4 && ge(r, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), h & /*margin*/
      1 && He(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: Ue,
    o: Ue,
    d(m) {
      m && sl(e);
    }
  };
}
function dl(n, e, t) {
  let l, i, { margin: f = !0 } = e;
  const s = Ge([0, 0]);
  Re(n, s, (c) => t(1, l = c));
  const o = Ge([0, 0]);
  Re(n, o, (c) => t(2, i = c));
  let r;
  async function _() {
    await Promise.all([s.set([125, 140]), o.set([-125, -140])]), await Promise.all([s.set([-125, 140]), o.set([125, -140])]), await Promise.all([s.set([-125, 0]), o.set([125, -0])]), await Promise.all([s.set([125, 0]), o.set([-125, 0])]);
  }
  async function a() {
    await _(), r || a();
  }
  async function d() {
    await Promise.all([s.set([125, 0]), o.set([-125, 0])]), a();
  }
  return ul(() => (d(), () => r = !0)), n.$$set = (c) => {
    "margin" in c && t(0, f = c.margin);
  }, [f, l, i, s, o];
}
class ml extends fl {
  constructor(e) {
    super(), rl(this, e, dl, cl, al, { margin: 0 });
  }
}
const {
  SvelteComponent: bl,
  append: Q,
  attr: D,
  binding_callbacks: Qe,
  check_outros: ht,
  create_component: gl,
  create_slot: pl,
  destroy_component: kl,
  destroy_each: wt,
  detach: w,
  element: J,
  empty: re,
  ensure_array_like: we,
  get_all_dirty_from_scope: hl,
  get_slot_changes: wl,
  group_outros: yt,
  init: yl,
  insert: y,
  mount_component: vl,
  noop: qe,
  safe_not_equal: ql,
  set_data: P,
  set_style: Y,
  space: I,
  text: C,
  toggle_class: B,
  transition_in: se,
  transition_out: oe,
  update_slot_base: jl
} = window.__gradio__svelte__internal, { tick: Cl } = window.__gradio__svelte__internal, { onDestroy: zl } = window.__gradio__svelte__internal, Fl = (n) => ({}), We = (n) => ({});
function xe(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l[40] = t, l;
}
function $e(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l;
}
function Ll(n) {
  let e, t = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, f;
  const s = (
    /*#slots*/
    n[29].error
  ), o = pl(
    s,
    n,
    /*$$scope*/
    n[28],
    We
  );
  return {
    c() {
      e = J("span"), l = C(t), i = I(), o && o.c(), D(e, "class", "error svelte-1txqlrd");
    },
    m(r, _) {
      y(r, e, _), Q(e, l), y(r, i, _), o && o.m(r, _), f = !0;
    },
    p(r, _) {
      (!f || _[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      r[1]("common.error") + "") && P(l, t), o && o.p && (!f || _[0] & /*$$scope*/
      268435456) && jl(
        o,
        s,
        r,
        /*$$scope*/
        r[28],
        f ? wl(
          s,
          /*$$scope*/
          r[28],
          _,
          Fl
        ) : hl(
          /*$$scope*/
          r[28]
        ),
        We
      );
    },
    i(r) {
      f || (se(o, r), f = !0);
    },
    o(r) {
      oe(o, r), f = !1;
    },
    d(r) {
      r && (w(e), w(i)), o && o.d(r);
    }
  };
}
function Sl(n) {
  let e, t, l, i, f, s, o, r, _, a = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && et(n)
  );
  function d(u, g) {
    if (
      /*progress*/
      u[7]
    )
      return Al;
    if (
      /*queue_position*/
      u[2] !== null && /*queue_size*/
      u[3] !== void 0 && /*queue_position*/
      u[2] >= 0
    )
      return Nl;
    if (
      /*queue_position*/
      u[2] === 0
    )
      return Vl;
  }
  let c = d(n), m = c && c(n), h = (
    /*timer*/
    n[5] && nt(n)
  );
  const v = [Tl, Pl], z = [];
  function j(u, g) {
    return (
      /*last_progress_level*/
      u[15] != null ? 0 : (
        /*show_progress*/
        u[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = j(n)) && (s = z[f] = v[f](n));
  let b = !/*timer*/
  n[5] && at(n);
  return {
    c() {
      a && a.c(), e = I(), t = J("div"), m && m.c(), l = I(), h && h.c(), i = I(), s && s.c(), o = I(), b && b.c(), r = re(), D(t, "class", "progress-text svelte-1txqlrd"), B(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), B(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(u, g) {
      a && a.m(u, g), y(u, e, g), y(u, t, g), m && m.m(t, null), Q(t, l), h && h.m(t, null), y(u, i, g), ~f && z[f].m(u, g), y(u, o, g), b && b.m(u, g), y(u, r, g), _ = !0;
    },
    p(u, g) {
      /*variant*/
      u[8] === "default" && /*show_eta_bar*/
      u[18] && /*show_progress*/
      u[6] === "full" ? a ? a.p(u, g) : (a = et(u), a.c(), a.m(e.parentNode, e)) : a && (a.d(1), a = null), c === (c = d(u)) && m ? m.p(u, g) : (m && m.d(1), m = c && c(u), m && (m.c(), m.m(t, l))), /*timer*/
      u[5] ? h ? h.p(u, g) : (h = nt(u), h.c(), h.m(t, null)) : h && (h.d(1), h = null), (!_ || g[0] & /*variant*/
      256) && B(
        t,
        "meta-text-center",
        /*variant*/
        u[8] === "center"
      ), (!_ || g[0] & /*variant*/
      256) && B(
        t,
        "meta-text",
        /*variant*/
        u[8] === "default"
      );
      let V = f;
      f = j(u), f === V ? ~f && z[f].p(u, g) : (s && (yt(), oe(z[V], 1, 1, () => {
        z[V] = null;
      }), ht()), ~f ? (s = z[f], s ? s.p(u, g) : (s = z[f] = v[f](u), s.c()), se(s, 1), s.m(o.parentNode, o)) : s = null), /*timer*/
      u[5] ? b && (b.d(1), b = null) : b ? b.p(u, g) : (b = at(u), b.c(), b.m(r.parentNode, r));
    },
    i(u) {
      _ || (se(s), _ = !0);
    },
    o(u) {
      oe(s), _ = !1;
    },
    d(u) {
      u && (w(e), w(t), w(i), w(o), w(r)), a && a.d(u), m && m.d(), h && h.d(), ~f && z[f].d(u), b && b.d(u);
    }
  };
}
function et(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = J("div"), D(e, "class", "eta-bar svelte-1txqlrd"), Y(e, "transform", t);
    },
    m(l, i) {
      y(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && Y(e, "transform", t);
    },
    d(l) {
      l && w(e);
    }
  };
}
function Vl(n) {
  let e;
  return {
    c() {
      e = C("processing |");
    },
    m(t, l) {
      y(t, e, l);
    },
    p: qe,
    d(t) {
      t && w(e);
    }
  };
}
function Nl(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, s;
  return {
    c() {
      e = C("queue: "), l = C(t), i = C("/"), f = C(
        /*queue_size*/
        n[3]
      ), s = C(" |");
    },
    m(o, r) {
      y(o, e, r), y(o, l, r), y(o, i, r), y(o, f, r), y(o, s, r);
    },
    p(o, r) {
      r[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      o[2] + 1 + "") && P(l, t), r[0] & /*queue_size*/
      8 && P(
        f,
        /*queue_size*/
        o[3]
      );
    },
    d(o) {
      o && (w(e), w(l), w(i), w(f), w(s));
    }
  };
}
function Al(n) {
  let e, t = we(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = lt($e(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = re();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = we(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const o = $e(i, t, s);
          l[s] ? l[s].p(o, f) : (l[s] = lt(o), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && w(e), wt(l, i);
    }
  };
}
function tt(n) {
  let e, t = (
    /*p*/
    n[38].unit + ""
  ), l, i, f = " ", s;
  function o(a, d) {
    return (
      /*p*/
      a[38].length != null ? Bl : Ml
    );
  }
  let r = o(n), _ = r(n);
  return {
    c() {
      _.c(), e = I(), l = C(t), i = C(" | "), s = C(f);
    },
    m(a, d) {
      _.m(a, d), y(a, e, d), y(a, l, d), y(a, i, d), y(a, s, d);
    },
    p(a, d) {
      r === (r = o(a)) && _ ? _.p(a, d) : (_.d(1), _ = r(a), _ && (_.c(), _.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      a[38].unit + "") && P(l, t);
    },
    d(a) {
      a && (w(e), w(l), w(i), w(s)), _.d(a);
    }
  };
}
function Ml(n) {
  let e = le(
    /*p*/
    n[38].index || 0
  ) + "", t;
  return {
    c() {
      t = C(e);
    },
    m(l, i) {
      y(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = le(
        /*p*/
        l[38].index || 0
      ) + "") && P(t, e);
    },
    d(l) {
      l && w(t);
    }
  };
}
function Bl(n) {
  let e = le(
    /*p*/
    n[38].index || 0
  ) + "", t, l, i = le(
    /*p*/
    n[38].length
  ) + "", f;
  return {
    c() {
      t = C(e), l = C("/"), f = C(i);
    },
    m(s, o) {
      y(s, t, o), y(s, l, o), y(s, f, o);
    },
    p(s, o) {
      o[0] & /*progress*/
      128 && e !== (e = le(
        /*p*/
        s[38].index || 0
      ) + "") && P(t, e), o[0] & /*progress*/
      128 && i !== (i = le(
        /*p*/
        s[38].length
      ) + "") && P(f, i);
    },
    d(s) {
      s && (w(t), w(l), w(f));
    }
  };
}
function lt(n) {
  let e, t = (
    /*p*/
    n[38].index != null && tt(n)
  );
  return {
    c() {
      t && t.c(), e = re();
    },
    m(l, i) {
      t && t.m(l, i), y(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].index != null ? t ? t.p(l, i) : (t = tt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && w(e), t && t.d(l);
    }
  };
}
function nt(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = C(
        /*formatted_timer*/
        n[20]
      ), l = C(t), i = C("s");
    },
    m(f, s) {
      y(f, e, s), y(f, l, s), y(f, i, s);
    },
    p(f, s) {
      s[0] & /*formatted_timer*/
      1048576 && P(
        e,
        /*formatted_timer*/
        f[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && P(l, t);
    },
    d(f) {
      f && (w(e), w(l), w(i));
    }
  };
}
function Pl(n) {
  let e, t;
  return e = new ml({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      gl(e.$$.fragment);
    },
    m(l, i) {
      vl(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), e.$set(f);
    },
    i(l) {
      t || (se(e.$$.fragment, l), t = !0);
    },
    o(l) {
      oe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      kl(e, l);
    }
  };
}
function Tl(n) {
  let e, t, l, i, f, s = `${/*last_progress_level*/
  n[15] * 100}%`, o = (
    /*progress*/
    n[7] != null && it(n)
  );
  return {
    c() {
      e = J("div"), t = J("div"), o && o.c(), l = I(), i = J("div"), f = J("div"), D(t, "class", "progress-level-inner svelte-1txqlrd"), D(f, "class", "progress-bar svelte-1txqlrd"), Y(f, "width", s), D(i, "class", "progress-bar-wrap svelte-1txqlrd"), D(e, "class", "progress-level svelte-1txqlrd");
    },
    m(r, _) {
      y(r, e, _), Q(e, t), o && o.m(t, null), Q(e, l), Q(e, i), Q(i, f), n[30](f);
    },
    p(r, _) {
      /*progress*/
      r[7] != null ? o ? o.p(r, _) : (o = it(r), o.c(), o.m(t, null)) : o && (o.d(1), o = null), _[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      r[15] * 100}%`) && Y(f, "width", s);
    },
    i: qe,
    o: qe,
    d(r) {
      r && w(e), o && o.d(), n[30](null);
    }
  };
}
function it(n) {
  let e, t = we(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = _t(xe(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = re();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = we(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const o = xe(i, t, s);
          l[s] ? l[s].p(o, f) : (l[s] = _t(o), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && w(e), wt(l, i);
    }
  };
}
function ft(n) {
  let e, t, l, i, f = (
    /*i*/
    n[40] !== 0 && Zl()
  ), s = (
    /*p*/
    n[38].desc != null && st(n)
  ), o = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && ot()
  ), r = (
    /*progress_level*/
    n[14] != null && rt(n)
  );
  return {
    c() {
      f && f.c(), e = I(), s && s.c(), t = I(), o && o.c(), l = I(), r && r.c(), i = re();
    },
    m(_, a) {
      f && f.m(_, a), y(_, e, a), s && s.m(_, a), y(_, t, a), o && o.m(_, a), y(_, l, a), r && r.m(_, a), y(_, i, a);
    },
    p(_, a) {
      /*p*/
      _[38].desc != null ? s ? s.p(_, a) : (s = st(_), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      _[38].desc != null && /*progress_level*/
      _[14] && /*progress_level*/
      _[14][
        /*i*/
        _[40]
      ] != null ? o || (o = ot(), o.c(), o.m(l.parentNode, l)) : o && (o.d(1), o = null), /*progress_level*/
      _[14] != null ? r ? r.p(_, a) : (r = rt(_), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(_) {
      _ && (w(e), w(t), w(l), w(i)), f && f.d(_), s && s.d(_), o && o.d(_), r && r.d(_);
    }
  };
}
function Zl(n) {
  let e;
  return {
    c() {
      e = C(" /");
    },
    m(t, l) {
      y(t, e, l);
    },
    d(t) {
      t && w(e);
    }
  };
}
function st(n) {
  let e = (
    /*p*/
    n[38].desc + ""
  ), t;
  return {
    c() {
      t = C(e);
    },
    m(l, i) {
      y(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[38].desc + "") && P(t, e);
    },
    d(l) {
      l && w(t);
    }
  };
}
function ot(n) {
  let e;
  return {
    c() {
      e = C("-");
    },
    m(t, l) {
      y(t, e, l);
    },
    d(t) {
      t && w(e);
    }
  };
}
function rt(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = C(e), l = C("%");
    },
    m(i, f) {
      y(i, t, f), y(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && P(t, e);
    },
    d(i) {
      i && (w(t), w(l));
    }
  };
}
function _t(n) {
  let e, t = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && ft(n)
  );
  return {
    c() {
      t && t.c(), e = re();
    },
    m(l, i) {
      t && t.m(l, i), y(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? t ? t.p(l, i) : (t = ft(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && w(e), t && t.d(l);
    }
  };
}
function at(n) {
  let e, t;
  return {
    c() {
      e = J("p"), t = C(
        /*loading_text*/
        n[9]
      ), D(e, "class", "loading svelte-1txqlrd");
    },
    m(l, i) {
      y(l, e, i), Q(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && P(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && w(e);
    }
  };
}
function El(n) {
  let e, t, l, i, f;
  const s = [Sl, Ll], o = [];
  function r(_, a) {
    return (
      /*status*/
      _[4] === "pending" ? 0 : (
        /*status*/
        _[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = r(n)) && (l = o[t] = s[t](n)), {
    c() {
      e = J("div"), l && l.c(), D(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), B(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), B(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), B(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), B(
        e,
        "border",
        /*border*/
        n[12]
      ), Y(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Y(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(_, a) {
      y(_, e, a), ~t && o[t].m(e, null), n[31](e), f = !0;
    },
    p(_, a) {
      let d = t;
      t = r(_), t === d ? ~t && o[t].p(_, a) : (l && (yt(), oe(o[d], 1, 1, () => {
        o[d] = null;
      }), ht()), ~t ? (l = o[t], l ? l.p(_, a) : (l = o[t] = s[t](_), l.c()), se(l, 1), l.m(e, null)) : l = null), (!f || a[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      _[8] + " " + /*show_progress*/
      _[6] + " svelte-1txqlrd")) && D(e, "class", i), (!f || a[0] & /*variant, show_progress, status, show_progress*/
      336) && B(e, "hide", !/*status*/
      _[4] || /*status*/
      _[4] === "complete" || /*show_progress*/
      _[6] === "hidden"), (!f || a[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && B(
        e,
        "translucent",
        /*variant*/
        _[8] === "center" && /*status*/
        (_[4] === "pending" || /*status*/
        _[4] === "error") || /*translucent*/
        _[11] || /*show_progress*/
        _[6] === "minimal"
      ), (!f || a[0] & /*variant, show_progress, status*/
      336) && B(
        e,
        "generating",
        /*status*/
        _[4] === "generating"
      ), (!f || a[0] & /*variant, show_progress, border*/
      4416) && B(
        e,
        "border",
        /*border*/
        _[12]
      ), a[0] & /*absolute*/
      1024 && Y(
        e,
        "position",
        /*absolute*/
        _[10] ? "absolute" : "static"
      ), a[0] & /*absolute*/
      1024 && Y(
        e,
        "padding",
        /*absolute*/
        _[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(_) {
      f || (se(l), f = !0);
    },
    o(_) {
      oe(l), f = !1;
    },
    d(_) {
      _ && w(e), ~t && o[t].d(), n[31](null);
    }
  };
}
let pe = [], ye = !1;
async function Dl(n, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (pe.push(n), !ye)
      ye = !0;
    else
      return;
    await Cl(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let l = 0; l < pe.length; l++) {
        const f = pe[l].getBoundingClientRect();
        (l === 0 || f.top + window.scrollY <= t[0]) && (t[0] = f.top + window.scrollY, t[1] = l);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), ye = !1, pe = [];
    });
  }
}
function Il(n, e, t) {
  let l, { $$slots: i = {}, $$scope: f } = e, { i18n: s } = e, { eta: o = null } = e, { queue_position: r } = e, { queue_size: _ } = e, { status: a } = e, { scroll_to_output: d = !1 } = e, { timer: c = !0 } = e, { show_progress: m = "full" } = e, { message: h = null } = e, { progress: v = null } = e, { variant: z = "default" } = e, { loading_text: j = "Loading..." } = e, { absolute: b = !0 } = e, { translucent: u = !1 } = e, { border: g = !1 } = e, { autoscroll: V } = e, k, _e = !1, me = 0, U = 0, x = null, $ = null, Se = 0, H = null, ae, K = null, Ve = !0;
  const vt = () => {
    t(0, o = t(26, x = t(19, be = null))), t(24, me = performance.now()), t(25, U = 0), _e = !0, Ne();
  };
  function Ne() {
    requestAnimationFrame(() => {
      t(25, U = (performance.now() - me) / 1e3), _e && Ne();
    });
  }
  function Ae() {
    t(25, U = 0), t(0, o = t(26, x = t(19, be = null))), _e && (_e = !1);
  }
  zl(() => {
    _e && Ae();
  });
  let be = null;
  function qt(p) {
    Qe[p ? "unshift" : "push"](() => {
      K = p, t(16, K), t(7, v), t(14, H), t(15, ae);
    });
  }
  function jt(p) {
    Qe[p ? "unshift" : "push"](() => {
      k = p, t(13, k);
    });
  }
  return n.$$set = (p) => {
    "i18n" in p && t(1, s = p.i18n), "eta" in p && t(0, o = p.eta), "queue_position" in p && t(2, r = p.queue_position), "queue_size" in p && t(3, _ = p.queue_size), "status" in p && t(4, a = p.status), "scroll_to_output" in p && t(21, d = p.scroll_to_output), "timer" in p && t(5, c = p.timer), "show_progress" in p && t(6, m = p.show_progress), "message" in p && t(22, h = p.message), "progress" in p && t(7, v = p.progress), "variant" in p && t(8, z = p.variant), "loading_text" in p && t(9, j = p.loading_text), "absolute" in p && t(10, b = p.absolute), "translucent" in p && t(11, u = p.translucent), "border" in p && t(12, g = p.border), "autoscroll" in p && t(23, V = p.autoscroll), "$$scope" in p && t(28, f = p.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (o === null && t(0, o = x), o != null && x !== o && (t(27, $ = (performance.now() - me) / 1e3 + o), t(19, be = $.toFixed(1)), t(26, x = o))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && t(17, Se = $ === null || $ <= 0 || !U ? null : Math.min(U / $, 1)), n.$$.dirty[0] & /*progress*/
    128 && v != null && t(18, Ve = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (v != null ? t(14, H = v.map((p) => {
      if (p.index != null && p.length != null)
        return p.index / p.length;
      if (p.progress != null)
        return p.progress;
    })) : t(14, H = null), H ? (t(15, ae = H[H.length - 1]), K && (ae === 0 ? t(16, K.style.transition = "0", K) : t(16, K.style.transition = "150ms", K))) : t(15, ae = void 0)), n.$$.dirty[0] & /*status*/
    16 && (a === "pending" ? vt() : Ae()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && k && d && (a === "pending" || a === "complete") && Dl(k, V), n.$$.dirty[0] & /*status, message*/
    4194320, n.$$.dirty[0] & /*timer_diff*/
    33554432 && t(20, l = U.toFixed(1));
  }, [
    o,
    s,
    r,
    _,
    a,
    c,
    m,
    v,
    z,
    j,
    b,
    u,
    g,
    k,
    H,
    ae,
    K,
    Se,
    Ve,
    be,
    l,
    d,
    h,
    V,
    me,
    U,
    x,
    $,
    f,
    i,
    qt,
    jt
  ];
}
class Jl extends bl {
  constructor(e) {
    super(), yl(
      this,
      e,
      Il,
      El,
      ql,
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
  SvelteComponent: Kl,
  assign: Ol,
  check_outros: Xl,
  create_component: ze,
  destroy_component: Fe,
  detach: Yl,
  get_spread_object: Gl,
  get_spread_update: Rl,
  group_outros: Ul,
  init: Hl,
  insert: Ql,
  mount_component: Le,
  safe_not_equal: Wl,
  space: xl,
  transition_in: ne,
  transition_out: ue
} = window.__gradio__svelte__internal;
function ut(n) {
  let e, t;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[8].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[8].i18n
    ) },
    /*loading_status*/
    n[7]
  ];
  let i = {};
  for (let f = 0; f < l.length; f += 1)
    i = Ol(i, l[f]);
  return e = new Jl({ props: i }), {
    c() {
      ze(e.$$.fragment);
    },
    m(f, s) {
      Le(e, f, s), t = !0;
    },
    p(f, s) {
      const o = s & /*gradio, loading_status*/
      384 ? Rl(l, [
        s & /*gradio*/
        256 && { autoscroll: (
          /*gradio*/
          f[8].autoscroll
        ) },
        s & /*gradio*/
        256 && { i18n: (
          /*gradio*/
          f[8].i18n
        ) },
        s & /*loading_status*/
        128 && Gl(
          /*loading_status*/
          f[7]
        )
      ]) : {};
      e.$set(o);
    },
    i(f) {
      t || (ne(e.$$.fragment, f), t = !0);
    },
    o(f) {
      ue(e.$$.fragment, f), t = !1;
    },
    d(f) {
      Fe(e, f);
    }
  };
}
function $l(n) {
  let e, t, l, i = (
    /*loading_status*/
    n[7] && ut(n)
  );
  return t = new dt({ props: { json: (
    /*value*/
    n[3]
  ) } }), {
    c() {
      i && i.c(), e = xl(), ze(t.$$.fragment);
    },
    m(f, s) {
      i && i.m(f, s), Ql(f, e, s), Le(t, f, s), l = !0;
    },
    p(f, s) {
      /*loading_status*/
      f[7] ? i ? (i.p(f, s), s & /*loading_status*/
      128 && ne(i, 1)) : (i = ut(f), i.c(), ne(i, 1), i.m(e.parentNode, e)) : i && (Ul(), ue(i, 1, 1, () => {
        i = null;
      }), Xl());
      const o = {};
      s & /*value*/
      8 && (o.json = /*value*/
      f[3]), t.$set(o);
    },
    i(f) {
      l || (ne(i), ne(t.$$.fragment, f), l = !0);
    },
    o(f) {
      ue(i), ue(t.$$.fragment, f), l = !1;
    },
    d(f) {
      f && Yl(e), i && i.d(f), Fe(t, f);
    }
  };
}
function en(n) {
  let e, t;
  return e = new el({
    props: {
      visible: (
        /*visible*/
        n[2]
      ),
      elem_id: (
        /*elem_id*/
        n[0]
      ),
      elem_classes: (
        /*elem_classes*/
        n[1]
      ),
      container: (
        /*container*/
        n[4]
      ),
      scale: (
        /*scale*/
        n[5]
      ),
      min_width: (
        /*min_width*/
        n[6]
      ),
      $$slots: { default: [$l] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      ze(e.$$.fragment);
    },
    m(l, i) {
      Le(e, l, i), t = !0;
    },
    p(l, [i]) {
      const f = {};
      i & /*visible*/
      4 && (f.visible = /*visible*/
      l[2]), i & /*elem_id*/
      1 && (f.elem_id = /*elem_id*/
      l[0]), i & /*elem_classes*/
      2 && (f.elem_classes = /*elem_classes*/
      l[1]), i & /*container*/
      16 && (f.container = /*container*/
      l[4]), i & /*scale*/
      32 && (f.scale = /*scale*/
      l[5]), i & /*min_width*/
      64 && (f.min_width = /*min_width*/
      l[6]), i & /*$$scope, value, gradio, loading_status*/
      904 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (ne(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ue(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Fe(e, l);
    }
  };
}
function tn(n, e, t) {
  let { elem_id: l = "" } = e, { elem_classes: i = [] } = e, { visible: f = !0 } = e, { value: s = !1 } = e, { container: o = !0 } = e, { scale: r = null } = e, { min_width: _ = void 0 } = e, { loading_status: a } = e, { gradio: d } = e;
  return n.$$set = (c) => {
    "elem_id" in c && t(0, l = c.elem_id), "elem_classes" in c && t(1, i = c.elem_classes), "visible" in c && t(2, f = c.visible), "value" in c && t(3, s = c.value), "container" in c && t(4, o = c.container), "scale" in c && t(5, r = c.scale), "min_width" in c && t(6, _ = c.min_width), "loading_status" in c && t(7, a = c.loading_status), "gradio" in c && t(8, d = c.gradio);
  }, [
    l,
    i,
    f,
    s,
    o,
    r,
    _,
    a,
    d
  ];
}
class ln extends Kl {
  constructor(e) {
    super(), Hl(this, e, tn, en, Wl, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      value: 3,
      container: 4,
      scale: 5,
      min_width: 6,
      loading_status: 7,
      gradio: 8
    });
  }
}
export {
  ln as default
};
