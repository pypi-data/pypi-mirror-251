const {
  SvelteComponent: c,
  append: u,
  attr: o,
  detach: r,
  element: d,
  init: g,
  insert: y,
  noop: f,
  safe_not_equal: v,
  set_data: m,
  text: b,
  toggle_class: i
} = window.__gradio__svelte__internal;
function h(a) {
  let e, n;
  return {
    c() {
      e = d("pre"), n = b(
        /*value*/
        a[0]
      ), o(e, "class", "svelte-1ioyqn2"), i(
        e,
        "table",
        /*type*/
        a[1] === "table"
      ), i(
        e,
        "gallery",
        /*type*/
        a[1] === "gallery"
      ), i(
        e,
        "selected",
        /*selected*/
        a[2]
      );
    },
    m(t, l) {
      y(t, e, l), u(e, n);
    },
    p(t, [l]) {
      l & /*value*/
      1 && m(
        n,
        /*value*/
        t[0]
      ), l & /*type*/
      2 && i(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), l & /*type*/
      2 && i(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), l & /*selected*/
      4 && i(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    i: f,
    o: f,
    d(t) {
      t && r(e);
    }
  };
}
function p(a, e, n) {
  let { value: t } = e, { type: l } = e, { selected: _ = !1 } = e;
  return a.$$set = (s) => {
    "value" in s && n(0, t = s.value), "type" in s && n(1, l = s.type), "selected" in s && n(2, _ = s.selected);
  }, [t, l, _];
}
class q extends c {
  constructor(e) {
    super(), g(this, e, p, h, v, { value: 0, type: 1, selected: 2 });
  }
}
export {
  q as default
};
