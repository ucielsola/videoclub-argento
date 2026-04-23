<script>
  import "../app.css";
  let { children } = $props();
</script>

<div class="h-dvh bg-gradient-to-br from-gray-50 via-indigo-50/30 to-purple-50/20 dark:from-gray-800 dark:via-indigo-900/30 dark:to-purple-900/20 relative flex flex-col">
  <div class="absolute inset-0 bg-grid-pattern opacity-[0.03] dark:opacity-[0.05]" />
  {@render children()}
</div>
