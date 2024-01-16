
Designed for medical imaging data preprocesing, two types of normalization are implemented:

1) Medical imaging mask inerpolation. 
2) SR image interpolation through Z directions (i.e., thick-slices to thin-slices) with arbitrary user-selected sampling ratios.


from KevinSR import mask_interpolation, SOUP_GAN

# for mask interp

new_masks = mask_interpolation(masks, factor)

# for SR image interp

thin_slices = SOUP_GAN(thick_slices, factor, prep_type)

#prep_type = 0 or 1 for different preprocessing types (thick-to-thin or thin-to-thin).


