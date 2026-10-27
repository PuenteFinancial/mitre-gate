// V02 closing band. "See our offering" goes back up to the homepage's offering.
function mount(root, ctx) {
  const btn = root.getElementById("ctaOffering");
  const onClick = () => { if (ctx && ctx.scrollTo) ctx.scrollTo("pillars") || ctx.scrollTo("proof"); };
  btn.addEventListener("click", onClick);
  return function cleanup() { btn.removeEventListener("click", onClick); };
}

export default mount;
