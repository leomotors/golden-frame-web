<script lang="ts">
  import frames from "../data.g.json";

  import clsx from "clsx/lite";

  let selectedFrame = "golden_frame.png";
  $: currentInfo = frames.find((frame) => frame.name === selectedFrame);

  let inputImage = "honami-base.jpg";
  let outputImage = "honami-golden-frame.jpg";
  $: outputDefined = outputImage !== "honami-golden-frame.jpg";

  let selectedImage: FileList;
  let inputFileName = "";

  let generateBtnEnabled = true;

  $: {
    if (selectedImage) {
      const reader = new FileReader();
      reader.onload = () => {
        inputImage = reader.result as string;
      };
      reader.readAsDataURL(selectedImage[0]);
      inputFileName = selectedImage[0].name;
      generateBtnEnabled = true;
    }
  }

  let errorMessage = "";
  // @ts-ignore intellisense bruh
  const apiPath = import.meta.env.DEV ? "http://localhost:3131/api" : "/api";

  async function handleSubmit() {
    generateBtnEnabled = false;

    const formData = new FormData();
    formData.append("frame_name", selectedFrame);
    formData.append("file", selectedImage[0]);

    const result = await fetch(apiPath, {
      method: "POST",
      body: formData,
    });

    if (result.ok) {
      const blob = await result.blob();
      outputImage = URL.createObjectURL(blob);
    } else {
      errorMessage = `${result.status} ${
        result.statusText
      } ${await result.text()}`;
    }
  }
</script>

<div class="flex items-center justify-center gap-4">
  <img class="max-w-xs" src="frames/{selectedFrame}" alt={currentInfo?.name} />

  <p class="text-5xl font-bold">+</p>

  <img class="max-w-xs" src={inputImage} alt="User Input" />

  <p class="text-5xl font-bold">=</p>

  <img class="max-w-xs" src={outputImage} alt="Generated Output" />
</div>

{#if errorMessage}
  <p class="mt-8 text-center text-red-500">{errorMessage}</p>
{/if}

<form
  class="mt-8 flex flex-col items-center gap-4"
  method="POST"
  action="/api"
  on:submit|preventDefault={handleSubmit}
>
  <div class="flex items-center justify-center">
    <label for="frameName" class="mr-2">Frame Name:</label>
    <select
      id="frameName"
      class="rounded-md border border-gray-300 px-2 py-1"
      bind:value={selectedFrame}
    >
      {#each frames as frame}
        <option value={frame.name}>{frame.name}</option>
      {/each}
    </select>
  </div>

  <div class="mt-4 flex items-center justify-center">
    <label for="inputImage" class="mr-2">Input Image:</label>
    <input
      type="file"
      accept=".jpeg, .jpg, .png, .webp, .avif"
      id="inputImage"
      class="rounded-md border border-gray-300 px-2 py-1"
      required
      bind:files={selectedImage}
    />
  </div>

  <div class="flex justify-center gap-4">
    <button
      type="submit"
      class="rounded bg-blue-500 px-4 py-2 font-bold text-white enabled:hover:bg-blue-600 disabled:bg-gray-500"
      disabled={!generateBtnEnabled}
    >
      Generate
    </button>

    <a
      href={outputDefined ? outputImage : "#"}
      download={outputDefined
        ? `${selectedFrame.split(".")[0]}-${inputFileName.split(".")[0]}.png`
        : undefined}
      class={clsx(
        "rounded px-4 py-2 font-bold text-white",
        outputDefined ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-500",
      )}
    >
      Save Image
    </a>
  </div>
</form>
