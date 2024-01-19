var I;
(function(e) {
  e.LOAD = "LOAD", e.EXEC = "EXEC", e.WRITE_FILE = "WRITE_FILE", e.READ_FILE = "READ_FILE", e.DELETE_FILE = "DELETE_FILE", e.RENAME = "RENAME", e.CREATE_DIR = "CREATE_DIR", e.LIST_DIR = "LIST_DIR", e.DELETE_DIR = "DELETE_DIR", e.ERROR = "ERROR", e.DOWNLOAD = "DOWNLOAD", e.PROGRESS = "PROGRESS", e.LOG = "LOG", e.MOUNT = "MOUNT", e.UNMOUNT = "UNMOUNT";
})(I || (I = {}));
function z(e, { autoplay: n }) {
  async function l() {
    n && await e.play();
  }
  return e.addEventListener("loadeddata", l), {
    destroy() {
      e.removeEventListener("loadeddata", l);
    }
  };
}
const { setContext: Ve, getContext: j } = window.__gradio__svelte__internal, H = "WORKER_PROXY_CONTEXT_KEY";
function B() {
  return j(H);
}
function J(e) {
  return e.host === window.location.host || e.host === "localhost:7860" || e.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  e.host === "lite.local";
}
function Q(e, n) {
  const l = n.toLowerCase();
  for (const [t, i] of Object.entries(e))
    if (t.toLowerCase() === l)
      return i;
}
function Z(e) {
  if (e == null)
    return !1;
  const n = new URL(e);
  return !(!J(n) || n.protocol !== "http:" && n.protocol !== "https:");
}
async function M(e) {
  if (e == null || !Z(e))
    return e;
  const n = B();
  if (n == null)
    return e;
  const t = new URL(e).pathname;
  return n.httpRequest({
    method: "GET",
    path: t,
    headers: {},
    query_string: ""
  }).then((i) => {
    if (i.status !== 200)
      throw new Error(`Failed to get file ${t} from the Wasm worker.`);
    const _ = new Blob([i.body], {
      type: Q(i.headers, "content-type")
    });
    return URL.createObjectURL(_);
  });
}
const {
  SvelteComponent: F,
  action_destroyer: x,
  add_render_callback: $,
  assign: D,
  attr: v,
  binding_callbacks: ee,
  create_slot: ne,
  detach: L,
  element: C,
  exclude_internal_props: N,
  get_all_dirty_from_scope: te,
  get_slot_changes: le,
  init: ie,
  insert: O,
  is_function: oe,
  listen: b,
  raf: ae,
  run_all: ue,
  safe_not_equal: se,
  space: de,
  src_url_equal: T,
  toggle_class: A,
  transition_in: re,
  transition_out: fe,
  update_slot_base: _e
} = window.__gradio__svelte__internal, { createEventDispatcher: ce } = window.__gradio__svelte__internal;
function me(e) {
  let n, l, t, i, _, c = !1, d, a = !0, r, o, E, R;
  const h = (
    /*#slots*/
    e[16].default
  ), m = ne(
    h,
    e,
    /*$$scope*/
    e[15],
    null
  );
  function g() {
    cancelAnimationFrame(d), t.paused || (d = ae(g), c = !0), e[17].call(t);
  }
  return {
    c() {
      n = C("div"), n.innerHTML = '<span class="load-wrap svelte-1pwzuub"><span class="loader svelte-1pwzuub"></span></span>', l = de(), t = C("video"), m && m.c(), v(n, "class", "overlay svelte-1pwzuub"), A(n, "hidden", !/*processingVideo*/
      e[9]), T(t.src, i = /*resolved_src*/
      e[10]) || v(t, "src", i), t.muted = /*muted*/
      e[4], t.playsInline = /*playsinline*/
      e[5], v(
        t,
        "preload",
        /*preload*/
        e[6]
      ), t.autoplay = /*autoplay*/
      e[7], t.controls = /*controls*/
      e[8], v(t, "data-testid", _ = /*$$props*/
      e[12]["data-testid"]), v(t, "crossorigin", "anonymous"), /*duration*/
      e[1] === void 0 && $(() => (
        /*video_durationchange_handler*/
        e[18].call(t)
      ));
    },
    m(u, f) {
      O(u, n, f), O(u, l, f), O(u, t, f), m && m.m(t, null), e[20](t), o = !0, E || (R = [
        b(
          t,
          "loadeddata",
          /*dispatch*/
          e[11].bind(null, "loadeddata")
        ),
        b(
          t,
          "click",
          /*dispatch*/
          e[11].bind(null, "click")
        ),
        b(
          t,
          "play",
          /*dispatch*/
          e[11].bind(null, "play")
        ),
        b(
          t,
          "pause",
          /*dispatch*/
          e[11].bind(null, "pause")
        ),
        b(
          t,
          "ended",
          /*dispatch*/
          e[11].bind(null, "ended")
        ),
        b(
          t,
          "mouseover",
          /*dispatch*/
          e[11].bind(null, "mouseover")
        ),
        b(
          t,
          "mouseout",
          /*dispatch*/
          e[11].bind(null, "mouseout")
        ),
        b(
          t,
          "focus",
          /*dispatch*/
          e[11].bind(null, "focus")
        ),
        b(
          t,
          "blur",
          /*dispatch*/
          e[11].bind(null, "blur")
        ),
        b(t, "timeupdate", g),
        b(
          t,
          "durationchange",
          /*video_durationchange_handler*/
          e[18]
        ),
        b(
          t,
          "play",
          /*video_play_pause_handler*/
          e[19]
        ),
        b(
          t,
          "pause",
          /*video_play_pause_handler*/
          e[19]
        ),
        x(r = z.call(null, t, { autoplay: (
          /*autoplay*/
          e[7] ?? !1
        ) }))
      ], E = !0);
    },
    p(u, [f]) {
      (!o || f & /*processingVideo*/
      512) && A(n, "hidden", !/*processingVideo*/
      u[9]), m && m.p && (!o || f & /*$$scope*/
      32768) && _e(
        m,
        h,
        u,
        /*$$scope*/
        u[15],
        o ? le(
          h,
          /*$$scope*/
          u[15],
          f,
          null
        ) : te(
          /*$$scope*/
          u[15]
        ),
        null
      ), (!o || f & /*resolved_src*/
      1024 && !T(t.src, i = /*resolved_src*/
      u[10])) && v(t, "src", i), (!o || f & /*muted*/
      16) && (t.muted = /*muted*/
      u[4]), (!o || f & /*playsinline*/
      32) && (t.playsInline = /*playsinline*/
      u[5]), (!o || f & /*preload*/
      64) && v(
        t,
        "preload",
        /*preload*/
        u[6]
      ), (!o || f & /*autoplay*/
      128) && (t.autoplay = /*autoplay*/
      u[7]), (!o || f & /*controls*/
      256) && (t.controls = /*controls*/
      u[8]), (!o || f & /*$$props*/
      4096 && _ !== (_ = /*$$props*/
      u[12]["data-testid"])) && v(t, "data-testid", _), !c && f & /*currentTime*/
      1 && !isNaN(
        /*currentTime*/
        u[0]
      ) && (t.currentTime = /*currentTime*/
      u[0]), c = !1, f & /*paused*/
      4 && a !== (a = /*paused*/
      u[2]) && t[a ? "pause" : "play"](), r && oe(r.update) && f & /*autoplay*/
      128 && r.update.call(null, { autoplay: (
        /*autoplay*/
        u[7] ?? !1
      ) });
    },
    i(u) {
      o || (re(m, u), o = !0);
    },
    o(u) {
      fe(m, u), o = !1;
    },
    d(u) {
      u && (L(n), L(l), L(t)), m && m.d(u), e[20](null), E = !1, ue(R);
    }
  };
}
function be(e, n, l) {
  let { $$slots: t = {}, $$scope: i } = n, { src: _ = void 0 } = n, { muted: c = void 0 } = n, { playsinline: d = void 0 } = n, { preload: a = void 0 } = n, { autoplay: r = void 0 } = n, { controls: o = void 0 } = n, { currentTime: E = void 0 } = n, { duration: R = void 0 } = n, { paused: h = void 0 } = n, { node: m = void 0 } = n, { processingVideo: g = !1 } = n, u, f;
  const P = ce();
  function X() {
    E = this.currentTime, l(0, E);
  }
  function G() {
    R = this.duration, l(1, R);
  }
  function K() {
    h = this.paused, l(2, h);
  }
  function w(s) {
    ee[s ? "unshift" : "push"](() => {
      m = s, l(3, m);
    });
  }
  return e.$$set = (s) => {
    l(12, n = D(D({}, n), N(s))), "src" in s && l(13, _ = s.src), "muted" in s && l(4, c = s.muted), "playsinline" in s && l(5, d = s.playsinline), "preload" in s && l(6, a = s.preload), "autoplay" in s && l(7, r = s.autoplay), "controls" in s && l(8, o = s.controls), "currentTime" in s && l(0, E = s.currentTime), "duration" in s && l(1, R = s.duration), "paused" in s && l(2, h = s.paused), "node" in s && l(3, m = s.node), "processingVideo" in s && l(9, g = s.processingVideo), "$$scope" in s && l(15, i = s.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*src, latest_src*/
    24576) {
      l(10, u = _), l(14, f = _);
      const s = _;
      M(s).then((Y) => {
        f === s && l(10, u = Y);
      });
    }
  }, n = N(n), [
    E,
    R,
    h,
    m,
    c,
    d,
    a,
    r,
    o,
    g,
    u,
    P,
    n,
    _,
    f,
    i,
    t,
    X,
    G,
    K,
    w
  ];
}
class Ee extends F {
  constructor(n) {
    super(), ie(this, n, be, me, se, {
      src: 13,
      muted: 4,
      playsinline: 5,
      preload: 6,
      autoplay: 7,
      controls: 8,
      currentTime: 0,
      duration: 1,
      paused: 2,
      node: 3,
      processingVideo: 9
    });
  }
}
new Intl.Collator(0, { numeric: 1 }).compare;
const {
  SvelteComponent: he,
  add_flush_callback: ve,
  append: Re,
  attr: ye,
  bind: ge,
  binding_callbacks: Le,
  create_component: Oe,
  destroy_component: ke,
  detach: k,
  element: W,
  empty: pe,
  init: Ie,
  insert: p,
  is_function: U,
  mount_component: De,
  noop: S,
  safe_not_equal: Ce,
  set_data: Ne,
  text: Te,
  toggle_class: y,
  transition_in: V,
  transition_out: q
} = window.__gradio__svelte__internal;
function Ae(e) {
  let n, l;
  return {
    c() {
      n = W("div"), l = Te(
        /*value*/
        e[2]
      );
    },
    m(t, i) {
      p(t, n, i), Re(n, l);
    },
    p(t, i) {
      i & /*value*/
      4 && Ne(
        l,
        /*value*/
        t[2]
      );
    },
    i: S,
    o: S,
    d(t) {
      t && k(n);
    }
  };
}
function Ue(e) {
  var d;
  let n, l, t, i;
  function _(a) {
    e[6](a);
  }
  let c = {
    muted: !0,
    playsinline: !0,
    src: (
      /*samples_dir*/
      e[3] + /*value*/
      ((d = e[2]) == null ? void 0 : d.video.path)
    )
  };
  return (
    /*video*/
    e[4] !== void 0 && (c.node = /*video*/
    e[4]), l = new Ee({ props: c }), Le.push(() => ge(l, "node", _)), l.$on(
      "loadeddata",
      /*init*/
      e[5]
    ), l.$on("mouseover", function() {
      U(
        /*video*/
        e[4].play.bind(
          /*video*/
          e[4]
        )
      ) && e[4].play.bind(
        /*video*/
        e[4]
      ).apply(this, arguments);
    }), l.$on("mouseout", function() {
      U(
        /*video*/
        e[4].pause.bind(
          /*video*/
          e[4]
        )
      ) && e[4].pause.bind(
        /*video*/
        e[4]
      ).apply(this, arguments);
    }), {
      c() {
        n = W("div"), Oe(l.$$.fragment), ye(n, "class", "container svelte-13u05e4"), y(
          n,
          "table",
          /*type*/
          e[0] === "table"
        ), y(
          n,
          "gallery",
          /*type*/
          e[0] === "gallery"
        ), y(
          n,
          "selected",
          /*selected*/
          e[1]
        );
      },
      m(a, r) {
        p(a, n, r), De(l, n, null), i = !0;
      },
      p(a, r) {
        var E;
        e = a;
        const o = {};
        r & /*samples_dir, value*/
        12 && (o.src = /*samples_dir*/
        e[3] + /*value*/
        ((E = e[2]) == null ? void 0 : E.video.path)), !t && r & /*video*/
        16 && (t = !0, o.node = /*video*/
        e[4], ve(() => t = !1)), l.$set(o), (!i || r & /*type*/
        1) && y(
          n,
          "table",
          /*type*/
          e[0] === "table"
        ), (!i || r & /*type*/
        1) && y(
          n,
          "gallery",
          /*type*/
          e[0] === "gallery"
        ), (!i || r & /*selected*/
        2) && y(
          n,
          "selected",
          /*selected*/
          e[1]
        );
      },
      i(a) {
        i || (V(l.$$.fragment, a), i = !0);
      },
      o(a) {
        q(l.$$.fragment, a), i = !1;
      },
      d(a) {
        a && k(n), ke(l);
      }
    }
  );
}
function Se(e) {
  let n, l, t, i;
  const _ = [Ue, Ae], c = [];
  function d(a, r) {
    return 0;
  }
  return n = d(), l = c[n] = _[n](e), {
    c() {
      l.c(), t = pe();
    },
    m(a, r) {
      c[n].m(a, r), p(a, t, r), i = !0;
    },
    p(a, [r]) {
      l.p(a, r);
    },
    i(a) {
      i || (V(l), i = !0);
    },
    o(a) {
      q(l), i = !1;
    },
    d(a) {
      a && k(t), c[n].d(a);
    }
  };
}
function We(e, n, l) {
  let { type: t } = n, { selected: i = !1 } = n, { value: _ } = n, { samples_dir: c } = n, d;
  async function a() {
    l(4, d.muted = !0, d), l(4, d.playsInline = !0, d), l(4, d.controls = !1, d), d.setAttribute("muted", ""), await d.play(), d.pause();
  }
  function r(o) {
    d = o, l(4, d);
  }
  return e.$$set = (o) => {
    "type" in o && l(0, t = o.type), "selected" in o && l(1, i = o.selected), "value" in o && l(2, _ = o.value), "samples_dir" in o && l(3, c = o.samples_dir);
  }, [t, i, _, c, d, a, r];
}
class qe extends he {
  constructor(n) {
    super(), Ie(this, n, We, Se, Ce, {
      type: 0,
      selected: 1,
      value: 2,
      samples_dir: 3
    });
  }
}
export {
  qe as default
};
