from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


class BasketballCourt:
    ### Length is x, width is y
    ### All units are in meters
    ### Axis origin is center of court
    court_length = 28
    court_width = 15
    center_radius_outer = 4.8 - 3.60 / 2
    center_radius_inner = 3.60 / 2

    anclas_to_baseline = 2
    anclas_to_sideline = 2
    parquet_to_lines = 2

    baseline_to_rim = 1.575
    baseline_to_backboard = 1.2
    rim_radius = 0.23
    backboard_width = 1.8

    three_radius = 6.75
    three_lateral_margin = 0.9
    three_lateral_length = 3.0

    throw_in_line = 8.325  # this is measured from baseline
    throw_in_line_length = 0.15

    zone_length = 5.8
    zone_width = 4.9
    zone_radius = 1.8
    zone_no_charge = 1.25
    zone_no_charge_lateral = 0.375

    def __init__(self):
        pass

    def draw(cls, ax=None, color="gray", lw=1, grid_step=None):
        """Plot a full basketball court to axis.
        References:
            - http://savvastjortjoglou.com/nba-shot-sharts.html
            - https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjcoIW4xef3AhUEtqQKHdVwAc8QFnoECAgQAQ&url=https%3A%2F%2Fnz.basketball%2Fwp-content%2Fuploads%2F2020%2F02%2FFIBA-Basketball-Court-Dimensions.pdf&usg=AOvVaw0aO3XSw26jtwJz772thhPx
        """
        # If an axes object isn't provided to plot onto, just get current one
        if ax is None:
            ax = plt.gca()

        ### Create the basketball rim
        # Diameter of a rim is 18" so it has a radius of 9", which is a value
        # 7.5 in our coordinate system
        rim_l = Circle(
            (
                cls.anclas_to_baseline + cls.baseline_to_rim,
                0,
            ),
            radius=cls.rim_radius,
            linewidth=lw,
            edgecolor="red",
            fill=False,
        )
        rim_r = Circle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                0,
            ),
            radius=cls.rim_radius,
            linewidth=lw,
            edgecolor="red",
            fill=False,
        )
        # Base of the rim. Unifies the rim and the backboard
        baserim_l = Rectangle(
            (
                cls.anclas_to_baseline + cls.baseline_to_backboard,
                0,
            ),
            (cls.zone_no_charge_lateral - cls.rim_radius),
            0,
            linewidth=lw,
            color="red",
        )
        baserim_r = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_backboard,
                0,
            ),
            -(cls.zone_no_charge_lateral - cls.rim_radius),
            0,
            linewidth=lw,
            color="red",
        )
        # Create backboard
        backboard_l = Rectangle(
            (
                cls.anclas_to_baseline + cls.baseline_to_backboard,
                -(0 + cls.backboard_width / 2),
            ),
            0,
            cls.backboard_width,
            linewidth=lw,
            color="white",
        )
        backboard_r = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_backboard,
                -(0 + cls.backboard_width / 2),
            ),
            0,
            cls.backboard_width,
            linewidth=lw,
            color="white",
        )

        ### The paint
        # Create the inner box of the paint, widt=12ft, height=19ft
        inner_box_l = Rectangle(
            (
                cls.anclas_to_baseline,
                -(0 + cls.zone_width / 2),
            ),
            cls.zone_length,
            cls.zone_width,
            linewidth=lw,
            edgecolor="white",
            facecolor="black",
            fill=True,
        )
        inner_box_r = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length,
                -(0 + cls.zone_width / 2),
            ),
            -cls.zone_length,
            cls.zone_width,
            linewidth=lw,
            edgecolor="white",
            facecolor="black",
            fill=True,
        )
        # Create free throw top arc
        zone_arc_l = Arc(
            (
                cls.anclas_to_baseline + cls.zone_length,
                0,
            ),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=-90,
            theta2=90,
            linewidth=lw,
            color="white",
            fill=False,
        )
        zone_arc_r = Arc(
            (
                cls.anclas_to_baseline + cls.court_length - cls.zone_length,
                0,
            ),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=90,
            theta2=-90,
            linewidth=lw,
            color="white",
            fill=False,
        )
        zone_arc_dashed_l = Arc(
            (cls.anclas_to_baseline + cls.zone_length, 0),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=90,
            theta2=-90,
            linewidth=lw,
            color="white",
            fill=False,
            linestyle="dashed",
        )
        zone_arc_dashed_r = Arc(
            (cls.anclas_to_baseline + cls.court_length - cls.zone_length, 0),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=-90,
            theta2=90,
            linewidth=lw,
            color="white",
            fill=False,
            linestyle="dashed",
        )
        # Restricted Zone, it is an arc with 4ft radius from center of the rim
        restricted_l = Arc(
            (cls.anclas_to_baseline + cls.baseline_to_rim, 0),
            2 * cls.zone_no_charge,
            2 * cls.zone_no_charge,
            theta1=-90,
            theta2=90,
            linewidth=lw,
            color="white",
        )
        restricted_r = Arc(
            (cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim, 0),
            2 * cls.zone_no_charge,
            2 * cls.zone_no_charge,
            theta1=90,
            theta2=-90,
            linewidth=lw,
            color="white",
        )
        restricted_l_a = Rectangle(
            (cls.anclas_to_baseline + cls.baseline_to_rim, 0 + cls.zone_no_charge),
            -cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )
        restricted_l_b = Rectangle(
            (cls.anclas_to_baseline + cls.baseline_to_rim, 0 - cls.zone_no_charge),
            -cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )
        restricted_r_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                0 + cls.zone_no_charge,
            ),
            cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )
        restricted_r_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                0 - cls.zone_no_charge,
            ),
            cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )

        ### Three point line
        # angle = 180/np.pi*np.arctan(court_width/2-three_lateral_margin/(three_lateral_length-baseline_to_rim))
        three_arc_l = Arc(
            (cls.anclas_to_baseline + cls.baseline_to_rim, 0),
            2 * cls.three_radius,
            2 * cls.three_radius,
            theta1=-78,
            theta2=78,
            linewidth=lw,
            color="white",
        )
        three_arc_r = Arc(
            (cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim, 0),
            2 * cls.three_radius,
            2 * cls.three_radius,
            theta1=180 - 78,
            theta2=180 + 78,
            linewidth=lw,
            color="white",
        )
        corner_three_l_a = Rectangle(
            (
                cls.anclas_to_baseline,
                (0 + cls.court_width / 2 - cls.three_lateral_margin),
            ),
            cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )
        corner_three_l_b = Rectangle(
            (
                cls.anclas_to_baseline,
                (0 - cls.court_width / 2 + cls.three_lateral_margin),
            ),
            cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )
        corner_three_r_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length,
                (0 + cls.court_width / 2 - cls.three_lateral_margin),
            ),
            -cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )
        corner_three_r_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length,
                (0 - cls.court_width / 2 + cls.three_lateral_margin),
            ),
            -cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )

        ### Lines and center
        center_inner_arc = Circle(
            (
                cls.anclas_to_baseline + cls.court_length / 2,
                0,
            ),
            cls.center_radius_inner,
            linewidth=lw,
            edgecolor="white",
            fill=False,
            linestyle="dashed",
        )

        """img = Image.new("RGB", (20, 20))
        im_logo = Image.open("EscudoBSFerrol.JPG")
        img.paste(im_logo, (100, 100))
        img.save("image.png")
        https://facundoq.github.io/courses/aa2018/res/04_imagenes_numpy.html"""

        outer_lines_l = Rectangle(
            (cls.anclas_to_baseline, 0 + cls.court_width / 2),
            cls.court_length / 2,
            -cls.court_width,
            linewidth=lw,
            edgecolor="white",
            facecolor="burlywood",
            fill=True,
        )
        outer_lines_r = Rectangle(
            (cls.anclas_to_baseline + cls.court_length / 2, 0 + cls.court_width / 2),
            cls.court_length / 2,
            -cls.court_width,
            linewidth=lw,
            edgecolor="white",
            facecolor="burlywood",
            fill=True,
        )
        parquet_lines = Rectangle(
            (
                cls.anclas_to_baseline - cls.parquet_to_lines,
                0 + cls.court_width / 2 + cls.parquet_to_lines,
            ),
            cls.court_length + 2 * cls.parquet_to_lines,
            -(cls.court_width + 2 * cls.parquet_to_lines),
            linewidth=lw,
            edgecolor="white",
            facecolor="black",
            fill=True,
        )
        ### Throw in line
        throw_in_line_l_a = Rectangle(
            (cls.anclas_to_baseline + cls.throw_in_line, 0 + cls.court_width / 2),
            0,
            cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )
        throw_in_line_l_b = Rectangle(
            (cls.anclas_to_baseline + cls.throw_in_line, 0 - cls.court_width / 2),
            0,
            -cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )
        throw_in_line_r_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.throw_in_line,
                0 + cls.court_width / 2,
            ),
            0,
            cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )
        throw_in_line_r_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.throw_in_line,
                0 - cls.court_width / 2,
            ),
            0,
            -cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )

        ### List of the court elements to be plotted onto the axes
        court_elements = [
            parquet_lines,
            outer_lines_l,
            outer_lines_r,
            inner_box_l,
            inner_box_r,
            rim_l,
            rim_r,
            baserim_l,
            baserim_r,
            backboard_l,
            backboard_r,
            zone_arc_l,
            zone_arc_r,
            zone_arc_dashed_l,
            zone_arc_dashed_r,
            restricted_l,
            restricted_r,
            restricted_l_a,
            restricted_l_b,
            restricted_r_a,
            restricted_r_b,
            three_arc_l,
            three_arc_r,
            corner_three_l_a,
            corner_three_l_b,
            corner_three_r_a,
            corner_three_r_b,
            center_inner_arc,
            throw_in_line_l_a,
            throw_in_line_l_b,
            throw_in_line_r_a,
            throw_in_line_r_b,
        ]

        ### Grid
        """if grid_step and type(grid_step) in [int, float]:
            ax.hlines(
                y=np.arange(
                    0,
                    int(cls.court_width / 2 + cls.anclas_to_sideline + 0.5),
                    grid_step,
                ),
                xmin=0,
                xmax=cls.court_length + 2 * cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )
            ax.hlines(
                y=-np.arange(
                    0,
                    int(cls.court_width / 2 + cls.anclas_to_sideline + 0.5),
                    grid_step,
                ),
                xmin=0,
                xmax=cls.court_length + 2 * cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )

            ax.vlines(
                x=np.arange(
                    0, int(2 * cls.anclas_to_baseline + cls.court_length), grid_step
                ),
                ymin=-cls.court_width / 2 - cls.anclas_to_baseline,
                ymax=cls.court_width / 2 + cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )

        # Add the court elements onto the axes
        for element in court_elements:
            ax.add_patch(element)

        return ax"""

        if grid_step and type(grid_step) in [int, float]:
            ax.hlines(
                y=np.arange(
                    -(cls.court_width / 2 + cls.anclas_to_sideline),
                    int(cls.court_width + 2 * cls.anclas_to_sideline),
                    grid_step,
                ),
                xmin=0,
                xmax=cls.court_length + 2 * cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )

            ax.vlines(
                x=np.arange(
                    0, int(2 * cls.anclas_to_baseline + cls.court_length), grid_step
                ),
                ymin=-cls.court_width / 2 - cls.anclas_to_baseline,
                ymax=cls.court_width / 2 + cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )

        # Add the court elements onto the axes
        for element in court_elements:
            ax.add_patch(element)

        return ax


class BasketballCourt_White:
    ### Length is x, width is y
    ### All units are in meters
    ### Axis origin is center of court
    court_length = 28
    court_width = 15
    center_radius_outer = 4.8 - 3.60 / 2
    center_radius_inner = 3.60 / 2

    anclas_to_baseline = 2
    anclas_to_sideline = 2

    baseline_to_rim = 1.575
    baseline_to_backboard = 1.2
    rim_radius = 0.23
    backboard_width = 1.8

    three_radius = 6.75
    three_lateral_margin = 0.9
    three_lateral_length = 3.0

    throw_in_line = 8.325  # this is measured from baseline
    throw_in_line_length = 0.15

    zone_length = 5.8
    zone_width = 4.9
    zone_radius = 1.8
    zone_no_charge = 1.25
    zone_no_charge_lateral = 0.375

    def __init__(self):
        pass

    def draw(cls, ax=None, color="gray", lw=1, grid_step=None):
        """Plot a full basketball court to axis.
        References:
            - http://savvastjortjoglou.com/nba-shot-sharts.html
            - https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjcoIW4xef3AhUEtqQKHdVwAc8QFnoECAgQAQ&url=https%3A%2F%2Fnz.basketball%2Fwp-content%2Fuploads%2F2020%2F02%2FFIBA-Basketball-Court-Dimensions.pdf&usg=AOvVaw0aO3XSw26jtwJz772thhPx
        """
        # If an axes object isn't provided to plot onto, just get current one
        if ax is None:
            ax = plt.gca()

        ### Create the basketball rim
        # Diameter of a rim is 18" so it has a radius of 9", which is a value
        # 7.5 in our coordinate system
        rim_l = Circle(
            (
                cls.anclas_to_baseline + cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            radius=cls.rim_radius,
            linewidth=lw,
            edgecolor="white",
            fill=False,
        )
        rim_r = Circle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            radius=cls.rim_radius,
            linewidth=lw,
            edgecolor="white",
            fill=False,
        )
        # Base of the rim. Unifies the rim and the backboard
        baserim_l = Rectangle(
            (
                cls.anclas_to_baseline + cls.baseline_to_backboard,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            (cls.zone_no_charge_lateral - cls.rim_radius),
            0,
            linewidth=lw,
            color="white",
        )
        baserim_r = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_backboard,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            -(cls.zone_no_charge_lateral - cls.rim_radius),
            0,
            linewidth=lw,
            color="white",
        )
        # Create backboard
        backboard_l = Rectangle(
            (
                cls.anclas_to_baseline + cls.baseline_to_backboard,
                (
                    cls.anclas_to_sideline
                    + cls.court_width / 2
                    - cls.backboard_width / 2
                ),
            ),
            0,
            cls.backboard_width,
            linewidth=lw,
            color="white",
        )
        backboard_r = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_backboard,
                (
                    cls.anclas_to_sideline
                    + cls.court_width / 2
                    - cls.backboard_width / 2
                ),
            ),
            0,
            cls.backboard_width,
            linewidth=lw,
            color="white",
        )

        ### The paint
        # Create the inner box of the paint, widt=12ft, height=19ft
        inner_box_l = Rectangle(
            (
                cls.anclas_to_baseline,
                (cls.anclas_to_sideline + cls.court_width / 2 - cls.zone_width / 2),
            ),
            cls.zone_length,
            cls.zone_width,
            linewidth=lw,
            edgecolor="white",
            fill=None,
        )
        inner_box_r = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length,
                (cls.anclas_to_sideline + cls.court_width / 2 - cls.zone_width / 2),
            ),
            -cls.zone_length,
            cls.zone_width,
            linewidth=lw,
            edgecolor="white",
            fill=None,
        )
        # Create free throw top arc
        zone_arc_l = Arc(
            (
                cls.anclas_to_baseline + cls.zone_length,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=-90,
            theta2=90,
            linewidth=lw,
            color="white",
            fill=False,
        )
        zone_arc_r = Arc(
            (
                cls.anclas_to_baseline + cls.court_length - cls.zone_length,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=90,
            theta2=-90,
            linewidth=lw,
            color="white",
            fill=False,
        )
        zone_arc_dashed_l = Arc(
            (
                cls.anclas_to_baseline + cls.zone_length,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=90,
            theta2=-90,
            linewidth=lw,
            color="white",
            fill=False,
            linestyle="dashed",
        )
        zone_arc_dashed_r = Arc(
            (
                cls.anclas_to_baseline + cls.court_length - cls.zone_length,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.zone_radius,
            2 * cls.zone_radius,
            theta1=-90,
            theta2=90,
            linewidth=lw,
            color="white",
            fill=False,
            linestyle="dashed",
        )
        # Restricted Zone, it is an arc with 4ft radius from center of the rim
        restricted_l = Arc(
            (
                cls.anclas_to_baseline + cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.zone_no_charge,
            2 * cls.zone_no_charge,
            theta1=-90,
            theta2=90,
            linewidth=lw,
            color="white",
        )
        restricted_r = Arc(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.zone_no_charge,
            2 * cls.zone_no_charge,
            theta1=90,
            theta2=-90,
            linewidth=lw,
            color="white",
        )
        restricted_l_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2 + cls.zone_no_charge,
            ),
            -cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )
        restricted_l_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2 - cls.zone_no_charge,
            ),
            -cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )
        restricted_r_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2 + cls.zone_no_charge,
            ),
            cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )
        restricted_r_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2 - cls.zone_no_charge,
            ),
            cls.zone_no_charge_lateral,
            0,
            linewidth=1.4,
            color="white",
        )

        ### Three point line
        # angle = 180/np.pi*np.arctan(court_width/2-three_lateral_margin/(three_lateral_length-baseline_to_rim))
        three_arc_l = Arc(
            (
                cls.anclas_to_baseline + cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.three_radius,
            2 * cls.three_radius,
            theta1=-78,
            theta2=78,
            linewidth=lw,
            color="white",
        )
        three_arc_r = Arc(
            (
                cls.anclas_to_baseline + cls.court_length - cls.baseline_to_rim,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            2 * cls.three_radius,
            2 * cls.three_radius,
            theta1=180 - 78,
            theta2=180 + 78,
            linewidth=lw,
            color="white",
        )
        corner_three_l_a = Rectangle(
            (
                cls.anclas_to_baseline,
                (cls.anclas_to_sideline + cls.three_lateral_margin),
            ),
            cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )
        corner_three_l_b = Rectangle(
            (
                cls.anclas_to_baseline,
                (cls.anclas_to_sideline + cls.court_width - cls.three_lateral_margin),
            ),
            cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )
        corner_three_r_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length,
                (cls.anclas_to_sideline + cls.three_lateral_margin),
            ),
            -cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )
        corner_three_r_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length,
                (cls.anclas_to_sideline + cls.court_width - cls.three_lateral_margin),
            ),
            -cls.three_lateral_length,
            0,
            linewidth=lw,
            color="white",
        )

        ### Lines and center
        center_inner_arc = Circle(
            (
                cls.anclas_to_baseline + cls.court_length / 2,
                cls.anclas_to_sideline + cls.court_width / 2,
            ),
            cls.center_radius_inner,
            linewidth=lw,
            edgecolor="white",
            fill=False,
            linestyle="dashed",
        )

        """img = Image.new("RGB", (20, 20))
        im_logo = Image.open("EscudoBSFerrol.JPG")
        img.paste(im_logo, (100, 100))
        img.save("image.png")
        https://facundoq.github.io/courses/aa2018/res/04_imagenes_numpy.html"""

        outer_lines_l = Rectangle(
            (cls.anclas_to_baseline, cls.anclas_to_sideline + cls.court_width),
            cls.court_length / 2,
            -cls.court_width,
            linewidth=lw,
            edgecolor="white",
            facecolor=None,
            alpha=1,
            fill=None,
        )
        outer_lines_r = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length / 2,
                cls.anclas_to_sideline + cls.court_width,
            ),
            cls.court_length / 2,
            -cls.court_width,
            linewidth=lw,
            edgecolor="white",
            facecolor=None,
            alpha=1,
            fill=None,
        )

        ### Throw in line
        throw_in_line_l_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.throw_in_line,
                cls.anclas_to_sideline,
            ),
            0,
            -cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )
        throw_in_line_l_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.throw_in_line,
                cls.anclas_to_sideline + cls.court_width,
            ),
            0,
            cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )
        throw_in_line_r_a = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.throw_in_line,
                cls.anclas_to_sideline,
            ),
            0,
            -cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )
        throw_in_line_r_b = Rectangle(
            (
                cls.anclas_to_baseline + cls.court_length - cls.throw_in_line,
                cls.anclas_to_sideline + cls.court_width,
            ),
            0,
            cls.throw_in_line_length,
            linewidth=lw,
            color="white",
        )

        ### List of the court elements to be plotted onto the axes
        court_elements = [
            rim_l,
            rim_r,
            baserim_l,
            baserim_r,
            backboard_l,
            backboard_r,
            zone_arc_l,
            zone_arc_r,
            zone_arc_dashed_l,
            zone_arc_dashed_r,
            restricted_l,
            restricted_r,
            restricted_l_a,
            restricted_l_b,
            restricted_r_a,
            restricted_r_b,
            three_arc_l,
            three_arc_r,
            corner_three_l_a,
            corner_three_l_b,
            corner_three_r_a,
            corner_three_r_b,
            center_inner_arc,
            throw_in_line_l_a,
            throw_in_line_l_b,
            throw_in_line_r_a,
            throw_in_line_r_b,
            outer_lines_l,
            outer_lines_r,
            inner_box_l,
            inner_box_r,
        ]

        ### Grid
        if grid_step and type(grid_step) in [int, float]:
            ax.hlines(
                y=np.arange(
                    cls.anclas_to_sideline + cls.court_width,
                    int(cls.court_width / 2 + cls.anclas_to_sideline + 0.5),
                    grid_step,
                ),
                xmin=0,
                xmax=cls.court_length + 2 * cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )
            ax.hlines(
                y=-np.arange(
                    0,
                    int(cls.court_width / 2 + cls.anclas_to_sideline + 0.5),
                    grid_step,
                ),
                xmin=0,
                xmax=cls.court_length + 2 * cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )

            ax.vlines(
                x=np.arange(
                    0, int(2 * cls.anclas_to_baseline + cls.court_length), grid_step
                ),
                ymin=-cls.court_width / 2 - cls.anclas_to_baseline,
                ymax=cls.court_width / 2 + cls.anclas_to_baseline,
                colors="gray",
                linewidth=0.5,
                alpha=0.5,
            )

        # Add the court elements onto the axes
        for element in court_elements:
            ax.add_patch(element)

        return ax


def draw_court(ax=None, color="gray", lw=1.3, grid_step=1):
    """Plot a full basketball court to axis using BasketballCourt as source class.

    References:
        - http://savvastjortjoglou.com/nba-shot-sharts.html
        - https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjcoIW4xef3AhUEtqQKHdVwAc8QFnoECAgQAQ&url=https%3A%2F%2Fnz.basketball%2Fwp-content%2Fuploads%2F2020%2F02%2FFIBA-Basketball-Court-Dimensions.pdf&usg=AOvVaw0aO3XSw26jtwJz772thhPx
    """
    return BasketballCourt().draw(ax=ax, color=color, lw=lw, grid_step=grid_step)


def draw_court_white(ax=None, color="gray", lw=1.3, grid_step=1):
    """Plot a full basketball court to axis using BasketballCourt as source class.

    References:
        - http://savvastjortjoglou.com/nba-shot-sharts.html
        - https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjcoIW4xef3AhUEtqQKHdVwAc8QFnoECAgQAQ&url=https%3A%2F%2Fnz.basketball%2Fwp-content%2Fuploads%2F2020%2F02%2FFIBA-Basketball-Court-Dimensions.pdf&usg=AOvVaw0aO3XSw26jtwJz772thhPx
    """
    return BasketballCourt_White().draw(ax=ax, color=color, lw=lw, grid_step=grid_step)


class Ancla:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    def get_position(self):
        return self.x, self.y


def draw_anclas(
    ax=None,
    anclas=None,
    margin=1,
    ancla_size=0.5,
    fontsize=10,
    color="red",
    lw=1,
    name_root="A",
):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    court = BasketballCourt()

    """# 10 anclas
    if not anclas:
        # +- 0.5 únicamente para la representación gráfica
        ancla_1 = Ancla(
            0 + 0.5,
            0,
            1,
        )
        ancla_2 = Ancla(
            0 + court.anclas_to_baseline,
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            2,
        )
        ancla_3 = Ancla(
            0 + court.anclas_to_baseline,
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            3,
        )
        ancla_4 = Ancla(
            (court.anclas_to_baseline + court.throw_in_line),
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            4,
        )
        ancla_5 = Ancla(
            (court.anclas_to_baseline + court.throw_in_line),
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            5,
        )
        ancla_6 = Ancla(
            (court.court_length + court.anclas_to_baseline - court.throw_in_line),
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            6,
        )
        ancla_7 = Ancla(
            (court.court_length + court.anclas_to_baseline - court.throw_in_line),
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            7,
        )
        ancla_8 = Ancla(
            (
                court.court_length
                + 2 * court.anclas_to_baseline
                - court.anclas_to_baseline
            ),
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            8,
        )
        ancla_9 = Ancla(
            (
                court.court_length
                + 2 * court.anclas_to_baseline
                - court.anclas_to_baseline
            ),
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            9,
        )
        ancla_10 = Ancla(
            (+2 * court.anclas_to_baseline + court.court_length - 0.5),
            0,
            10,
        )
        anclas = {
            ancla_1.id: ancla_1,
            ancla_2.id: ancla_2,
            ancla_3.id: ancla_3,
            ancla_4.id: ancla_4,
            ancla_5.id: ancla_5,
            ancla_6.id: ancla_6,
            ancla_7.id: ancla_7,
            ancla_8.id: ancla_8,
            ancla_9.id: ancla_9,
            ancla_10.id: ancla_10,
        }"""

    """# 8 anclas
    if not anclas:
        # +- 0.5 únicamente para la representación gráfica
        ancla_1 = Ancla(
            0 + 0.5,
            0,
            1,
        )
        ancla_2 = Ancla(
            0 + court.anclas_to_baseline,
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            2,
        )
        ancla_3 = Ancla(
            0 + court.anclas_to_baseline,
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            3,
        )
        ancla_4 = Ancla(
            (court.anclas_to_baseline + court.court_length / 2),
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            4,
        )
        ancla_5 = Ancla(
            (court.anclas_to_baseline + court.court_length / 2),
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            5,
        )
        ancla_6 = Ancla(
            (
                court.court_length
                + 2 * court.anclas_to_baseline
                - court.anclas_to_baseline
            ),
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            6,
        )
        ancla_7 = Ancla(
            (
                court.court_length
                + 2 * court.anclas_to_baseline
                - court.anclas_to_baseline
            ),
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            7,
        )
        ancla_8 = Ancla(
            (+2 * court.anclas_to_baseline + court.court_length - 0.5),
            0,
            8,
        )
        anclas = {
            ancla_1.id: ancla_1,
            ancla_2.id: ancla_2,
            ancla_3.id: ancla_3,
            ancla_4.id: ancla_4,
            ancla_5.id: ancla_5,
            ancla_6.id: ancla_6,
            ancla_7.id: ancla_7,
            ancla_8.id: ancla_8,
        }"""

    # 6 anclas
    if not anclas:
        # +- 0.5 únicamente para la representación gráfica
        ancla_1 = Ancla(
            0 + 0.5,
            0,
            1,
        )
        ancla_2 = Ancla(
            (court.anclas_to_baseline + court.throw_in_line),
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            2,
        )
        ancla_3 = Ancla(
            (court.anclas_to_baseline + court.throw_in_line),
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            3,
        )
        ancla_4 = Ancla(
            (court.court_length + court.anclas_to_baseline - court.throw_in_line),
            (court.anclas_to_sideline + court.court_width / 2 - 0.5),
            4,
        )
        ancla_5 = Ancla(
            (court.court_length + court.anclas_to_baseline - court.throw_in_line),
            -(court.anclas_to_sideline + court.court_width / 2 - 0.5),
            5,
        )
        ancla_6 = Ancla(
            (+2 * court.anclas_to_baseline + court.court_length - 0.5),
            0,
            6,
        )
        anclas = {
            ancla_1.id: ancla_1,
            ancla_2.id: ancla_2,
            ancla_3.id: ancla_3,
            ancla_4.id: ancla_4,
            ancla_5.id: ancla_5,
            ancla_6.id: ancla_6,
        }

    """# 8 anclas (TomaDatos_2905)
    if not anclas:
        # +- 0.5 únicamente para la representación gráfica
        ancla_1 = Ancla(
            0 + 0.5,
            0,
            1,
        )
        ancla_2 = Ancla(
            court.anclas_to_baseline + 2.3,
            (court.court_width / 2 + court.anclas_to_baseline - 0.5),
            2,
        )
        ancla_3 = Ancla(
            court.anclas_to_baseline + 2.3,
            -(court.court_width / 2 + court.anclas_to_baseline - 0.5),
            3,
        )
        ancla_4 = Ancla(
            court.anclas_to_baseline + court.court_length / 2,
            (court.court_width / 2 + court.anclas_to_baseline - 0.5),
            4,
        )
        ancla_5 = Ancla(
            court.anclas_to_baseline + court.court_length / 2,
            -(court.court_width / 2 + court.anclas_to_baseline - 0.5),
            5,
        )
        ancla_6 = Ancla(
            court.anclas_to_baseline + court.court_length - 1.1,
            (court.court_width / 2 + court.anclas_to_baseline - 0.5),
            6,
        )
        ancla_7 = Ancla(
            court.anclas_to_baseline + court.court_length - 1.1,
            -(court.court_width / 2 + court.anclas_to_baseline - 0.5),
            7,
        )
        ancla_8 = Ancla(
            (+2 * court.anclas_to_baseline + court.court_length - 0.5),
            0,
            8,
        )
        anclas = {
            ancla_1.id: ancla_1,
            ancla_2.id: ancla_2,
            ancla_3.id: ancla_3,
            ancla_4.id: ancla_4,
            ancla_5.id: ancla_5,
            ancla_6.id: ancla_6,
            ancla_7.id: ancla_7,
            ancla_8.id: ancla_8,
        }"""

    ### List of the elements to be plotted onto the axes
    try:
        elements = [
            Circle(ancla.get_position(), ancla_size, linewidth=lw, color=color)
            for ancla in anclas.values()
        ]
    except AttributeError:
        elements = [
            Circle(ancla, ancla_size, linewidth=lw, color=color)
            for ancla in anclas.values()
        ]

    ### Add the elements onto the axes
    for i, element in enumerate(elements):
        ax.add_patch(element)
        ax.annotate(
            f"{name_root}{i+1}",
            element.get_center(),
            color="w",
            weight="bold",
            fontsize=fontsize,
            ha="center",
            va="center",
        )

    return ax


def draw_players(
    ax=None,
    positions=None,
    realtime=None,
    size=0.3,
    fontsize=5,
    color="green",
    lw=1,
    numero=None,
):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    ### List of the elements to be plotted onto the axes
    try:
        elements = [
            Circle(
                position.get_position(),
                size,
                linewidth=lw,
                color=color,
            )
            for position in positions.values()
        ]
    except AttributeError:
        elements = [
            Circle(
                position,
                size,
                linewidth=lw,
                color=color,
            )
            for position in positions.values()
        ]

    ### Add the elements onto the axes
    for i, element in enumerate(elements):
        ax.add_patch(element)
        ax.annotate(
            f"{numero}",
            element.get_center(),
            color="w",
            weight="bold",
            fontsize=fontsize,
            ha="center",
            va="center",
        )
    return ax


def draw_players_realtime(
    ax=None,
    posicion_x=None,
    posicion_y=None,
    numero=None,
    realtime=None,
    size=0.3,
    fontsize=7,
    edgecolor="white",
    facecolor="green",
    lw=1,
):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    if realtime == "Si":
        jugador.clear()

    jugador = Circle(
        [posicion_x, posicion_y],
        size,
        linewidth=lw,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(jugador)
    ax.annotate(
        f"{numero}",
        jugador.get_center(),
        color="white",
        weight="bold",
        fontsize=fontsize,
        ha="center",
        va="center",
    )


def draw_positions(grid_step=1):
    ax = plt.axes(xlim=(0, 32), ylim=(-9.5, 9.5))
    plt.title("PISTA COMPLETA")
    draw_court(ax, grid_step=grid_step)
    draw_anclas(ax)

    return ax


# PRUEBAS TFG CARLOS
if __name__ == "__main__":
    draw_positions()
    plt.show()
"""El draw_positions es únicamente para cuando NO le pasamos las posiciones de las anclas?¿Podríamos emplear esto para mostrar las posiciones del tag?"""
"""Habría que corregir las coordenadas de los puntos o de los ejes. TAMBIÉN VA A DEPENDER DE SI CAMBIAMOS O NO LAS ANCLAS"""
