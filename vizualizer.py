import matplotlib.pyplot as plt
import textwrap
from matplotlib.widgets import Button


def _caption_layout(caption, columns):
    width = max(18, 96 // columns)
    wrapped = textwrap.fill(str(caption), width=width)
    line_count = wrapped.count("\n") + 1
    fontsize = max(6, min(10, 10 - 0.6 * (line_count - 1)))
    return wrapped, fontsize


def vizualize(data):
    # Display up to 16 images with captions sized for the grid.
    rows = columns = 4
    fig, axes = plt.subplots(rows, columns, figsize=(14, 13))

    for i, ax in enumerate(axes.flat):
        if i < len(data):
            sample = data[i]
            ax.imshow(sample["image"])
            caption, fontsize = _caption_layout(sample["caption_0"], columns)
            ax.text(
                0.5,
                -0.05,
                caption,
                transform=ax.transAxes,
                ha="center",
                va="top",
                fontsize=fontsize,
                clip_on=False,
            )
        ax.axis("off")

    fig.subplots_adjust(bottom=0.16, hspace=0.65, wspace=0.15)
    plt.show()


class Visualizer:

    def __init__(self, data, x_grid, y_grid):
        if x_grid <= 0 or y_grid <= 0:
            raise ValueError("x_grid, and y_grid must be positive")

        self.__batch_size = x_grid * y_grid
        self.__current_index = 0
        self.__ds = data
        self.__fig, self.__axes = plt.subplots(
            x_grid, y_grid, figsize=(14, max(10, x_grid * 3.25)), squeeze=False
        )
        self.__fig.subplots_adjust(bottom=0.12, hspace=0.65, wspace=0.15)
        self.__buttons = ()


    def update_plot(self, start_idx):
        for i, ax in enumerate(self.__axes.flat):
            ax.clear()
            idx = start_idx + i
            if idx < len(self.__ds):
                sample = self.__ds[idx]
                ax.imshow(sample["image"])
                caption, fontsize = _caption_layout(
                    sample["caption_0"], self.__axes.shape[1]
                )
                ax.text(
                    0.5,
                    -0.05,
                    f"[{idx}] {caption}",
                    transform=ax.transAxes,
                    ha="center",
                    va="top",
                    fontsize=fontsize,
                    clip_on=False,
                )
            ax.axis("off")

        self.__fig.suptitle(
            (
                f"Showing images {start_idx} to "
                f"{min(start_idx + self.__batch_size, len(self.__ds)) - 1} "
                f"of {len(self.__ds)}"
                if len(self.__ds)
                else "No images (0 total)"
            ),
            fontsize=12,
            fontweight="bold",
        )
        self.__fig.canvas.draw_idle()


    def next_batch(self, event): # load the next batch by changing the current index
        if self.__current_index + self.__batch_size < len(self.__ds):
            self.__current_index += self.__batch_size
            self.update_plot(self.__current_index)


    def prev_batch(self, event): # load the prev batch by changing the current index
        if self.__current_index - self.__batch_size >= 0:
            self.__current_index -= self.__batch_size
            self.update_plot(self.__current_index)


    # Optional: Also support Left/Right arrow keys
    def on_key(self, event):
        if event.key == "right":
            self.next_batch(event)
        elif event.key == "left":
            self.prev_batch(event)

    def display(self):
        # Create button axes [left, bottom, width, height]
        ax_prev = self.__fig.add_axes([0.35, 0.02, 0.12, 0.05])
        ax_next = self.__fig.add_axes([0.53, 0.02, 0.12, 0.05])

        btn_prev = Button(ax_prev, "← Previous")
        btn_next = Button(ax_next, "Next →")

        btn_prev.on_clicked(self.prev_batch)
        btn_next.on_clicked(self.next_batch)
        self.__buttons = (btn_prev, btn_next)
        self.__fig.canvas.mpl_connect("key_press_event", self.on_key)

        # Render initial batch
        self.update_plot(self.__current_index)
        plt.show()