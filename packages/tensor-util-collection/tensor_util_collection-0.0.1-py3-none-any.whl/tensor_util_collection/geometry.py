import numpy as np
import torch
from .decorators import pytorch_precedence

def transform_points_numpy(points, transform):
    n_point_dims = len(points.shape) - 1
    n_channels = points.shape[-1] - 3
    points = np.atleast_2d(points)
    coords = points[..., :3]
    features = points[..., 3:] if n_channels > 0 else None
    ones = np.ones((*coords.shape[:-1], 1))
    # if no batch dims are present, create one
    n_transform_dims = len(transform.shape) - 2
    if n_transform_dims == 0:
        transform = transform[np.newaxis, ...]
    # align points and transform shapes for broadcasting
    transform = transform[(np.newaxis, )*max(n_point_dims, 1)]
    homogenized_coords = np.concatenate([coords, ones], axis=-1)
    homogenized_coords = homogenized_coords[(slice(None),)*max(n_point_dims, 1) + (np.newaxis, )*max(n_transform_dims, 1) + (slice(None),) + (np.newaxis, )]
    transformed_coords = (transform @ homogenized_coords)[...,:3,0]
    # assign features to transformed points if necessary
    if n_channels > 0:
        features = features[(slice(None),)*max(n_point_dims, 1) + (np.newaxis, )*max(n_transform_dims, 1)]
        features = np.broadcast_to(features, transformed_coords.shape[:-1] + (features.shape[-1],))
        transformed_points = np.concatenate([transformed_coords, features], axis=-1)
    else:
        transformed_points = transformed_coords
    # if batch dims were created, undo that
    if n_transform_dims == 0:
        transformed_points = np.squeeze(transformed_points, axis=max(n_point_dims, 1))
    if n_point_dims == 0:
        transformed_points = np.squeeze(transformed_points, axis=0)

    return transformed_points

@pytorch_precedence
def transform_points(points, transform, is_numpy=None):
    if is_numpy:
        return transform_points_numpy(points, transform)
    else:
        # if no batch dims are present, create one
        n_point_dims = len(points.shape) - 1
        n_channels = points.shape[-1] - 3
        points = torch.atleast_2d(points)
        coords = points[..., :3]
        features = points[..., 3:] if n_channels > 0 else None
        ones = torch.ones((*coords.shape[:-1], 1), device=coords.device)
        # if no batch dims are present, create one
        n_transform_dims = len(transform.shape) - 2
        if n_transform_dims == 0:
            transform = transform.unsqueeze(0)
        # allign points and transform shapes for broadcasting
        transform = transform[(None, )*max(n_point_dims,1)]
        homogenized_coords = torch.cat([coords, ones], dim=-1)[(slice(None),)*max(n_point_dims,1) + (None, )*max(n_transform_dims,1) + (slice(None),) + (None, )]
        transformed_coords = (transform @ homogenized_coords)[...,:3,0]
        # assign features to transformed points if necessary
        if n_channels > 0:
            features = features[(slice(None),)*max(n_point_dims,1) + (None, )*max(n_transform_dims,1)]
            features = features.expand(*transformed_coords.shape[:-1],-1)
            transformed_points = torch.cat([transformed_coords, features], dim=-1)
        else:
            transformed_points = transformed_coords
        # if batch dims were created, undo that
        if n_transform_dims == 0:
            transformed_points = transformed_points.squeeze(max(n_point_dims,1))
        if n_point_dims == 0:
            transformed_points = transformed_points.squeeze(0)
        
        return transformed_points
    
def transform_frames_numpy(frames, transform):
    # if no frame batch dims are present, create one
    n_frame_dims = len(frames.shape) - 2
    if n_frame_dims == 0:
        frames = frames[np.newaxis, ...]
    # if no transform batch dims are present, create one
    n_transform_dims = len(transform.shape) - 2
    if n_transform_dims == 0:
        transform = transform[np.newaxis, ...]
    # align frames and transform shapes for broadcasting
    transform = transform[(np.newaxis, )*max(n_frame_dims, 1)]
    frames = frames[(slice(None),)*max(n_frame_dims, 1) + (np.newaxis, )*max(n_transform_dims, 1)]
    transformed_frames = transform @ frames
    # if batch dims were created, undo that
    if n_transform_dims == 0:
        transformed_frames = np.squeeze(transformed_frames, axis=max(n_frame_dims, 1))
    if n_frame_dims == 0:
        transformed_frames = np.squeeze(transformed_frames, axis=0)

    return transformed_frames

@pytorch_precedence
def transform_frames(frames, transform, is_numpy=None):
    if is_numpy:
        return transform_frames_numpy(frames, transform)
    else:
        # if no frame batch dims are present, create one
        n_frame_dims = len(frames.shape) - 2
        if n_frame_dims == 0:
            frames = frames.unsqueeze(0)
        # if no transform batch dims are present, create one
        n_transform_dims = len(transform.shape) - 2
        if n_transform_dims == 0:
            transform = transform.unsqueeze(0)
        # allign frames and transform shapes for broadcasting
        transform = transform[(None, )*max(n_frame_dims,1)]
        frames = frames[(slice(None),)*max(n_frame_dims,1) + (None, )*max(n_transform_dims,1)]
        transformed_frames = transform @ frames
        # assign features to transformed points if necessary
        # if batch dims were created, undo that
        if n_transform_dims == 0:
            transformed_frames = transformed_frames.squeeze(max(n_frame_dims,1))
        if n_frame_dims == 0:
            transformed_frames = transformed_frames.squeeze(0)
        return transformed_frames
    
def invert_transform_numpy(transform):
    if transform.ndim < 2 or transform.shape[-2:] != (4, 4):
        raise ValueError("Input must be a 4x4 matrix or a batch of 4x4 matrices.")
    is_batch = transform.ndim != 2
    if not is_batch:
        transform = np.expand_dims(transform, 0)
    R = transform[..., :3, :3]
    t = transform[..., :3, 3]
    axes = list(range(transform.ndim))
    axes[-2], axes[-1] = axes[-1], axes[-2]
    R_inv = np.transpose(R, axes=axes)
    t_inv = -(R_inv@np.expand_dims(t, axis=-1))
    upper_part = np.concatenate([R_inv, t_inv], axis=-1)
    lower_part = np.array([0, 0, 0, 1], dtype=transform.dtype)
    lower_part = lower_part[(np.newaxis, )*(transform.ndim-2+1)]
    lower_part = np.broadcast_to(lower_part, transform.shape[:-2] +(1,4))
    transform_inv = np.concatenate([upper_part, lower_part], axis=-2)
    if not is_batch:
        transform_inv = np.squeeze(transform_inv, axis=0)
    return transform_inv

@pytorch_precedence
def invert_transform(transform, is_numpy=None):
    if is_numpy:
        return invert_transform_numpy(transform)
    else:
        if transform.dim() < 2 or transform.shape[-2:] != (4, 4):
            raise ValueError("Input must be a 4x4 matrix or a batch of 4x4 matrices.")
        is_batch = not transform.dim() == 2
        if not is_batch:
            transform = transform.unsqueeze(0)
        R = transform[..., :3, :3]
        t = transform[..., :3, 3]
        R_inv = R.transpose(-2, -1)
        t_inv = -(R_inv@t.unsqueeze(-1))
        upper_part = torch.cat([R_inv, t_inv], dim=-1)
        lower_part = torch.tensor([0, 0, 0, 1], dtype=transform.dtype, device=transform.device)
        lower_part = lower_part[(None, )*(transform.dim()-2+1)]
        lower_part = lower_part.expand(*transform.shape[:-2],1,-1)
        transform_inv = torch.cat([upper_part, lower_part], dim=-2)
        if not is_batch:
            transform_inv = transform_inv.squeeze(0)
        return transform_inv