# DiveEdit

DiveEdit is a Windows desktop app for turning diver communication footage into a clean report video. Import the raw videos, let DiveEdit find the spoken inspection sections, review the timeline, make manual adjustments, and export the final cut.

## Install

1. Open the latest GitHub Release.
2. Download `DiveEdit-Setup-0.1.0.exe`.
3. Run the installer.
4. Choose the default install path, or select another folder if you prefer.
5. Launch DiveEdit from the desktop shortcut or Start menu.

The first launch may take longer while DiveEdit prepares FFmpeg, GPU support when available, and the speech model cache.

## Quick Start

1. Click **Import**.
2. Select the folder that contains the raw job videos.
3. Fill in the title fields.
4. Check which videos should be included.
5. Click **Start Pipeline**.
6. Review the generated timeline.
7. Play any section that needs checking.
8. Trim, remove, or add clips if needed.
9. Click **Export**.

## Import

Use **Import** to choose a folder with raw `.avi` videos.

In the file list:

- Checked files can be used by the pipeline.
- Unchecked files are ignored.
- If an intro file is unchecked, DiveEdit will not force it into the result.
- Use select all / deselect all when the folder has many videos.

## Pipeline

The pipeline reads speech, detects the intro, checks timestamp order, and creates the first timeline.

The progress log shows:

- CUDA or CPU mode
- active worker count
- selected intro video
- timestamp check status
- generated clip count

If the intro cannot be detected automatically, improve the title fields or mark the intro file manually, then run the pipeline again.

## Timeline

Use the timeline to review and refine the cut.

Common actions:

- Click a clip to select it.
- Shift-click to select multiple clips.
- Drag a clip edge to trim it.
- Drag the playhead to preview a time.
- Right-click the timeline to open the context menu.
- Use **Remove** after selecting one or more clips.
- Hold Alt and use the mouse wheel or touchpad zoom gesture to zoom the video lane.
- Hold Shift and drag-scroll the timeline when zoomed in.

Very short clips may appear as compact color blocks instead of frame thumbnails. They can still be selected, trimmed, played, and removed.

## Preview

The preview box plays the selected clip or the clip under the playhead.

Controls:

- Play / pause
- Drag the progress bar to seek
- Hover the volume button to show volume control
- Drag the volume bar to adjust sound
- Change playback speed
- Expand to fullscreen preview

In fullscreen preview, the control panel appears near the bottom when the mouse moves into the control area or when playback is paused.

## Manual Editing

You can edit the timeline even without running the pipeline.

Useful cases:

- make a quick manual cut
- add a missed spoken section
- remove unwanted footage
- correct intro or body boundaries

Manual edits are saved with the job cache.

## Export

Click **Export** when the timeline is ready.

DiveEdit renders:

- title / cover segment
- overlay text
- logo placement
- selected timeline clips
- final report video

If export fails, check the progress log. Common causes are missing source videos, file permission issues, or interrupted setup downloads.

## Job Cache

DiveEdit stores working files inside the selected job folder:

```text
<job folder>/_diveedit/
```

This folder may contain transcripts, timeline data, thumbnails, preview cache, and logs. It can be deleted after the final video has been checked and no further edits are needed.

## Troubleshooting

If preview feels slow, wait for the loading indicator to finish before jumping quickly between clips.

If GPU mode is not available, DiveEdit falls back to CPU mode. CPU mode is slower but still works.

If the wrong intro is selected, make sure the title fields contain clear job, vessel, and work-scope keywords.

If a video is missing from the output, confirm it is checked in the import file list and still exists in the job folder.
