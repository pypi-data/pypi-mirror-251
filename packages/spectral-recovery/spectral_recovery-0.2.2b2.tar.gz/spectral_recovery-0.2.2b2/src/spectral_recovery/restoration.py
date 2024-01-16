"""Restoration Area and Reference System classes.

The RestorationArea class represents a restoration event and contains
methods for computing spectral recovery metrics. Users create a
RestorationArea by providing a restoration polygon, reference polygon,
event dates, and a stack of annual composites. 

A RestorationArea contains a ReferenceSystem, which is a class that
represents the reference area(s) and contains methods for computing
the recovery target. 

"""
from typing import Callable, Optional, Union, List
from datetime import datetime

import xarray as xr
import geopandas as gpd
import pandas as pd
from pandas import Index

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import seaborn as sns

from spectral_recovery.recovery_target import median_target
from spectral_recovery.timeseries import _SatelliteTimeSeries
from spectral_recovery.enums import Metric
from spectral_recovery._config import VALID_YEAR

from spectral_recovery import metrics as m


# We could maybe remove baseline_method as attribute. Just add it
# as a parameter to baseline()? Wait for more refactoring planning.
class _ReferenceSystem:
    """A Reference System.

    Attributes
    -----------
    reference_polygons : gpd.GeoDataframe
        The spatial deliniation of the reference areas. GeoDataframe
        must contain at least one geometry and must be
        of type shapely.Polygon or shapely.MultiPolygon
    reference_stack: xr.DataArray
        A 4D (band, time, y, x) DataArray of images from which indices and
        metrics will be computed. The spatial bounds of the DataArray must
        contain `restoration_polygon` and (optional) `reference_polygons`,
        and the temporal bounds must contain `restoration_start`.
    reference_years : Tuple of datetimes
        The year or range of years from which to get values for computing
        the recovery target.
    recovery_target_method : Callable
        The method for computing the recovery target value. Must operate on
        4D (band, time, y, x) DataArrays.

    """

    def __init__(
        self,
        reference_stack: xr.DataArray,
        reference_range: Union[datetime, List[datetime]],
        reference_polygons: gpd.GeoDataFrame,
        historic_reference_system: bool,
        recovery_target_method: Optional[Callable] = None,
    ) -> None:
        self.hist_ref_sys = historic_reference_system
        self.reference_polygons = reference_polygons
        self.reference_range = reference_range
        self.recovery_target_method = recovery_target_method or median_target

        try:
            if self._within(reference_stack):
                self.reference_stack = reference_stack
        except ValueError as e:
            raise e from None

        clipped_stacks = {}
        for i, row in reference_polygons.iterrows():
            polygon_stack = reference_stack.rio.clip(gpd.GeoSeries(row.geometry).values)
            clipped_stacks[i] = polygon_stack
        self.reference_stack = xr.concat(
            clipped_stacks.values(),
            dim=Index(clipped_stacks.keys(), name="poly_id"),
        )

    def recovery_target(self):
        """Get the recovery target for a reference system"""
        if self.hist_ref_sys:
            recovery_target = self.recovery_target_method(
                stack=self.reference_stack,
                reference_date=self.reference_range,
                space=False,
            )
        else:
            recovery_target = self.recovery_target_method(
                stack=self.reference_stack,
                reference_date=self.reference_range,
                space=True,
            )
        return recovery_target

    # TODO: Add method for plotting spectral trajectory of reference system

    def _within(self, stack: xr.DataArray) -> bool:
        """Check if within a DataArray

        Determines whether an RestorationArea's spatial (polygons) and temporal
        (reference and event years) attributes are contained within a
        stack of yearly composite images.

        """
        if not stack.satts.contains_spatial(self.reference_polygons):
            raise ValueError(
                "Reference polygon is not contained in the spatial bounds of the"
                " annual composite stack. The spatial bounds of the annual composite"
                f" stack are: {stack.rio.bounds()}"
            ) from None
        if not stack.satts.contains_temporal(self.reference_range):
            raise ValueError(
                "Reference range is not contained in the temporal bounds of the annual"
                " composite stack. The temporal bounds of the annual composite stack"
                f" are: {stack['time'].min().data} to {stack['time'].max().data}"
            ) from None
        return True


class RestorationArea:
    """A Restoration Area (RA).

    Attributes
    -----------
    restoration_polygon : GeoDataFrame
        The spatial deliniation of the restoration event. There
        must only be one geometry in the GeoDataframe and it must be
        of type shapely.Polygon or shapely.MultiPolygon.
    reference_polygon : GeoDataFrame
        The spatial delinitation of the reference area(s).
    reference_years : datetime or Tuple of datetimes
        The year or range of years from which to get values for computing
        the recovery target.
    composite_stack : xr.DataArray
        A 4D (band, time, y, x) DataArray of images from which indices and
        metrics will be computed. The spatial bounds of the DataArray must
        contain `restoration_polygon` and (optional) `reference_polygons`,
        and the temporal bounds must contain `restoration_start`.
    disturbance_start : str or datetime
        The year the disturbance began. Value must be within
        the time dimension coordinates of `composite_stack` param.
    restoration_start : str or datetime
        The year the restoration event began. Value must be within
        the time dimension coordinates of `composite_stack` param.

    """

    def __init__(
        self,
        restoration_polygon: gpd.GeoDataFrame,
        reference_years: str | List[str],
        composite_stack: xr.DataArray,
        reference_polygon: gpd.GeoDataFrame = None,
        disturbance_start: str = None,
        restoration_start: str = None,
    ) -> None:
        if restoration_polygon.shape[0] != 1:
            raise ValueError(
                "restoration_polygons contains more than one Polygon."
                "A RestorationArea instance can only contain one Polygon."
            ) from None
        self.restoration_polygon = restoration_polygon

        if disturbance_start is None and restoration_start is None:
            raise ValueError(
                "At least one of disturbance_start or restoration_start need to be set,"
                " both are None."
            ) from None
        if disturbance_start is not None:
            if not isinstance(disturbance_start, str):
                raise TypeError("disturbance_start must be a string.") from None

            year = VALID_YEAR.match(disturbance_start)
            if year:
                self.disturbance_start = pd.to_datetime(disturbance_start)
            else:
                raise ValueError(
                    "Could not parse {disturbance_start} into a year. Please ensure"
                    " the year is in the format 'YYYY'."
                )
            if restoration_start is None:
                self.restoration_start = pd.to_datetime(
                    str(self.disturbance_start.year + 1)
                )
                if self.restoration_start < self.disturbance_start:
                    raise ValueError(
                        "The disturbance start year must be less than the restoration"
                        " start year."
                    ) from None

        if restoration_start is not None:
            if not isinstance(restoration_start, str):
                raise TypeError("restoration_start must be a string.") from None
            year = VALID_YEAR.match(restoration_start)
            if year:
                self.restoration_start = pd.to_datetime(restoration_start)
            else:
                raise ValueError(
                    "Could not parse {restoration_start} into a year. Please ensure"
                    " the year is in the format 'YYYY'."
                )
            if disturbance_start is None:
                self.disturbance_start = pd.to_datetime(
                    str(self.restoration_start.year - 1)
                )

        if isinstance(reference_years, str):
            year = VALID_YEAR.match(reference_years)
            if year:
                self.reference_years = pd.to_datetime(reference_years)
        else:
            try:
                _ = iter(reference_years)
                if len(reference_years) == 2:
                    self.reference_years = [
                        pd.to_datetime(reference_years[0]),
                        pd.to_datetime(reference_years[1]),
                    ]
                else:
                    raise ValueError(
                        "reference_years must be a string or iterable of 2 strings."
                    ) from None
            except TypeError:
                raise TypeError(
                    "reference_years must be a string or iterable of 2 strings."
                ) from None

        if self.restoration_start < self.disturbance_start:
            raise ValueError(
                "The disturbance start year must be less than the restoration start"
                " year."
            )
        if composite_stack.satts.is_annual_composite:
            try:
                if self._within(composite_stack):
                    self.stack = composite_stack.rio.clip(
                        self.restoration_polygon.geometry.values
                    )
            except ValueError as e:
                raise e from None
        else:
            raise ValueError(
                "composite_stack is not a valid stack of annual composites. Please"
                " ensure there are no missing years and that the DataArray object"
                " contains 'band', 'time', 'y' and 'x' dimensions."
            ) from None

        if reference_polygon is None:
            # Build the reference polygon from the restoration polygon
            self.reference_system = _ReferenceSystem(
                reference_polygons=self.restoration_polygon,
                reference_range=self.reference_years,
                reference_stack=composite_stack,
                recovery_target_method=None,
                historic_reference_system=True,
            )
        else:
            # Build the reference polygon from the reference polygon
            # Use the unclipped composite_stack instead of self.stack because
            # self.stack is clipped to restoration_polygons at this point.
            self.reference_system = _ReferenceSystem(
                reference_polygons=reference_polygon,
                reference_range=self.reference_years,
                reference_stack=composite_stack,
                recovery_target_method=None,
                historic_reference_system=False,
            )

        self.end_year = pd.to_datetime(self.stack["time"].max().data)

    def _within(self, stack: xr.DataArray) -> bool:
        """Check if within a DataArray

        Determines whether an RestorationArea's spatial (polygons) and temporal
        (years) attributes are contained within a stack of annual composite images.

        """
        if not stack.satts.contains_spatial(self.restoration_polygon):
            raise ValueError(
                "Restoration polygon is not contained in the spatial bounds of the"
                " annual composite stack. The spatial bounds of the annual composite"
                f" stack are: {stack.rio.bounds()}"
            ) from None
        if not stack.satts.contains_temporal(self.restoration_start):
            raise ValueError(
                "Restoration start year is not contained in the temporal bounds of the"
                " annual composite stack. The temporal bounds of the annual composite"
                f" stack are: {stack['time'].min().data} to {stack['time'].max().data}"
            ) from None
        if not stack.satts.contains_temporal(self.disturbance_start):
            raise ValueError(
                "Disturbance start year is not contained in the temporal bounds of the"
                " annual composite stack. The temporal bounds of the annual composite"
                f" stack are: {stack['time'].min().data} to {stack['time'].max().data}"
            ) from None
        return True

    def y2r(self, percent_of_target: int = 80):
        """Compute the Years to Recovery (Y2R) metric."""
        post_restoration = self.stack.sel(
            time=slice(self.restoration_start, self.end_year)
        )
        recovery_target = self.reference_system.recovery_target()
        y2r = m.y2r(
            image_stack=post_restoration,
            recovery_target=recovery_target,
            rest_start=str(self.restoration_start.year),
            percent=percent_of_target,
        )
        y2r = y2r.expand_dims(dim={"metric": [Metric.Y2R]})
        return y2r

    def yryr(self, timestep: int = 5):
        """Compute the Relative Years to Recovery (YRYR) metric."""
        yryr = m.yryr(
            image_stack=self.stack,
            rest_start=str(self.restoration_start.year),
            timestep=timestep,
        )
        yryr = yryr.expand_dims(dim={"metric": [Metric.YRYR]})
        return yryr

    def dnbr(self, timestep: int = 5):
        """Compute the differenced normalized burn ratio (dNBR) metric."""
        dnbr = m.dnbr(
            image_stack=self.stack,
            rest_start=str(self.restoration_start.year),
            timestep=timestep,
        )
        dnbr = dnbr.expand_dims(dim={"metric": [Metric.DNBR]})
        return dnbr

    def _rri(self, timestep: int = 5):
        """Compute the relative recovery index (RRI) metric."""
        rri = m.rri(
            image_stack=self.stack,
            rest_start=str(self.restoration_start.year),
            dist_start=str(self.disturbance_start.year),
            timestep=timestep,
        )
        rri = rri.expand_dims(dim={"metric": [Metric.RRI]})
        return rri

    def r80p(self, percent_of_target: int = 80, timestep: int = 5):
        """Compute the recovery to 80% of target (R80P) metric."""
        recovery_target = self.reference_system.recovery_target()
        r80p = m.r80p(
            image_stack=self.stack,
            rest_start=str(self.restoration_start.year),
            recovery_target=recovery_target,
            timestep=timestep,
            percent=percent_of_target,
        )
        r80p = r80p.expand_dims(dim={"metric": [Metric.R80P]})
        return r80p

    # Slow, probably because of the pandas stuff
    def plot_spectral_trajectory(self, path: str = None) -> None:
        """Create spectral trajectory plot of the RestorationArea

        Parameters
        ----------
        path : str, optional
            The path to save the plot to.
        """

        stats = self.stack.satts.stats()
        stats = stats.sel(
            stats=[
                "median",
                "mean",
            ]
        )
        stats = stats.to_dataframe("value").reset_index()
        stats["time"] = stats["time"].dt.year

        reco_targets = self.reference_system.recovery_target()
        reco_targets = reco_targets.to_dataframe("reco_targets").reset_index()[
            ["band", "reco_targets"]
        ]
        stats = stats.merge(reco_targets, how="left", on="band")
        stats = stats.rename(columns={"stats": "Statistic"})

        # Set theme and colour palette for plots
        sns.set_theme()
        palette = sns.color_palette("deep")

        # Plot per-band statistic lineplots
        with sns.color_palette(palette):
            g = sns.FacetGrid(
                stats,
                col="band",
                hue="Statistic",
                sharey=False,
                sharex=False,
                height=5,
                aspect=1.5,
                legend_out=True,
            )
            g.map_dataframe(sns.lineplot, "time", "value")

        g.set(xticks=stats["time"].unique())
        g.set_xticklabels(rotation=45)

        # Add recovery target line
        g.map_dataframe(
            sns.lineplot,
            "time",
            "reco_targets",
            color="black",
            linestyle="dotted",
            lw=1,
        )
        for ax in g.axes.flat:
            ax.set_xlabel("Year")
        g.axes[0, 0].set_ylabel("Band/Index Value")

        # Plot spectral trajectory windows: reference, disturbance, recovery
        g.map(
            plt.axvline,
            x=self.restoration_start.year,
            color=palette[2],
            linestyle="dashed",
            lw=1,
        )
        g.map(
            plt.axvline,
            x=self.disturbance_start.year,
            color=palette[3],
            linestyle="dashed",
            lw=1,
        )
        if self.reference_system.hist_ref_sys:
            g.map(
                plt.axvline,
                x=self.reference_years[0].year,
                color=palette[4],
                linestyle="dashed",
                lw=1,
            )
            if self.reference_years[1].year != self.disturbance_start.year:
                g.map(
                    plt.axvline,
                    x=self.reference_years[1].year,
                    color=palette[4],
                    linestyle="dashed",
                    lw=1,
                )
        for ax in g.axes.flat:
            if self.reference_system.hist_ref_sys:
                ax.axvspan(
                    self.reference_years[0].year,
                    self.reference_years[1].year,
                    alpha=0.1,
                    color=palette[4],
                )
            ax.axvspan(
                self.disturbance_start.year,
                self.restoration_start.year,
                alpha=0.1,
                color=palette[3],
            )
            ax.axvspan(
                self.restoration_start.year,
                self.end_year.year,
                alpha=0.1,
                color=palette[2],
            )

        # Create custom legend for Facet grid.
        median_line = Line2D([0], [0], color=palette[0], lw=2)
        mean_line = Line2D([0], [0], color=palette[1], lw=2)
        recovery_target_line = Line2D([0], [0], color="black", linestyle="dotted", lw=1)
        recovery_target_patch = Patch(facecolor="black", alpha=0.4)

        recovery_window_line = Line2D(
            [0], [0], color=palette[2], linestyle="dashed", lw=1
        )
        recovery_window_patch = Patch(facecolor=palette[2], alpha=0.1)
        disturbance_window_line = Line2D(
            [0], [0], color=palette[3], linestyle="dashed", lw=1
        )
        disturbance_window_patch = Patch(facecolor=palette[3], alpha=0.1)
        reference_years = Line2D([0], [0], color=palette[4], linestyle="dashed", lw=1)
        reference_years_patch = Patch(facecolor=palette[4], alpha=0.1)

        custom_handles = [
            median_line,
            mean_line,
            (disturbance_window_line, disturbance_window_patch),
            (recovery_window_line, recovery_window_patch),
        ]

        labels = [
            "median",
            "mean",
            "disturbance window",
            "recovery window",
        ]
        if self.reference_system.hist_ref_sys:
            custom_handles.insert(
                2,
                (recovery_target_line, recovery_target_patch),
            )
            custom_handles.insert(3, (reference_years, reference_years_patch))
            labels.insert(2, "historic recovery target (mean)")
            labels.insert(3, "reference year(s)")

        else:
            custom_handles.insert(
                2,
                recovery_target_line,
            )
            labels.insert(2, "reference recovery target")

        plt.figlegend(
            labels=labels,
            handles=custom_handles,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.05),
            fancybox=True,
            ncol=6,
        )
        plt.suptitle("Spectral Trajectory of RestorationArea Site")
        plt.tight_layout()
        if path:
            plt.savefig(path, dpi=300, bbox_inches="tight")
        else:
            plt.show()
