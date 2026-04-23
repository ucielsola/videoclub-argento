<script>
  import "../app.css";
  let { children } = $props();
</script>

<div class="bg-white dark:bg-gray-900 relative min-h-dvh">
  {@render children()}
</div>
