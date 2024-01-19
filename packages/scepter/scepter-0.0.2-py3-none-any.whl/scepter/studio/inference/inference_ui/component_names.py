# -*- coding: utf-8 -*-
# For dataset manager


class InferenceUIName():
    def __init__(self, language='en'):
        if language == 'en':
            self.advance_block_name = 'Advance Setting'
            self.check_box_for_setting = [
                'Use Mantra', 'Use Tuners', 'Use Controller'
            ]
            self.diffusion_paras = 'Generation Setting'
            self.mantra_paras = 'Mantra Book'
            self.tuner_paras = 'Tuners'
            self.contrl_paras = 'Controlable Generation'
            self.refine_paras = 'Refiner Setting'
        elif language == 'zh':
            self.advance_block_name = '生成选项'
            self.check_box_for_setting = ['使用咒语', '使用微调', '使用控制']
            self.diffusion_paras = '生成参数设置'
            self.mantra_paras = '咒语书'
            self.tuner_paras = '微调模型'
            self.contrl_paras = '可控生成'
            self.refine_paras = 'Refine设置'


class ModelManageUIName():
    def __init__(self, language='en'):
        if language == 'en':
            self.model_block_name = 'Model Management'
            self.postprocess_model_name = 'Refiners and Tuners'
            self.diffusion_model = 'Unet'
            self.first_stage_model = 'Vae'
            self.cond_stage_model = 'Condition Model'
            self.refine_diffusion_model = 'Refine Unet'
            self.refine_cond_model = 'Refine Condition Model'
            self.load_lora_tuner = 'Load Lora Tuner'
            self.load_swift_tuner = 'Load swift Tuner'
        elif language == 'zh':
            self.model_block_name = '模型管理'
            self.postprocess_model_name = 'Refiners and Tuners'
            self.diffusion_model = 'Unet'
            self.first_stage_model = 'Vae'
            self.cond_stage_model = 'Condition Model'
            self.refine_diffusion_model = 'Refine Unet'
            self.refine_cond_model = 'Refine Condition Model'
            self.load_lora_tuner = '加载 Lora 微调模型'
            self.load_swift_tuner = '加载 Swift 微调模型'


class GalleryUIName():
    def __init__(self, language='en'):
        if language == 'en':
            self.gallery_block_name = "Model's Output"
            self.gallery_diffusion_output = 'Diffusion Output'
            self.gallery_before_refine_output = 'Before Refine Output'
            self.prompt_input = 'Type Prompt Here'
            self.generate = 'Generate'
        elif language == 'zh':
            self.gallery_block_name = '模型的输出'
            self.gallery_diffusion_output = '扩散输出'
            self.gallery_before_refine_output = '精炼前输出'
            self.prompt_input = '在此输入提示'
            self.generate = '生成'


class DiffusionUIName():
    def __init__(self, language='en'):
        if language == 'en':

            self.sample = 'Sampler'
            self.sample_steps = 'Sample Steps'
            self.image_number = 'Images Number'
            self.resolutions_height = 'Output Height'
            self.resolutions_width = 'Output Width'

            self.negative_prompt = 'Negative Prompt'
            self.negative_prompt_placeholder = 'Type Prompt Here'
            self.negative_prompt_description = 'Describing what you do not want to see.'
            self.prompt_prefix = 'Prompt Prefix'
            self.guide_scale = 'Guide Scale For Uncondition'
            self.guide_rescale = 'Guide ReScale'
            self.discretization = 'Discretization'
            self.random_seed = 'Use Random Seed'
            self.seed = 'Used Seed'

        elif language == 'zh':

            self.sample = '采样器'
            self.sample_steps = '采样步数'
            self.image_number = '图片数量'
            self.resolutions_height = '输出高度'
            self.resolutions_width = '输出宽度'
            self.negative_prompt = '负向提示'
            self.negative_prompt_placeholder = '在此输入提示'
            self.negative_prompt_description = '描述您不希望看到的内容。'
            self.prompt_prefix = '提示前缀词'
            self.guide_scale = '条件引导比例'
            self.guide_rescale = '引导缩放'
            self.discretization = '离散化'
            self.random_seed = '使用随机种子'
            self.seed = '使用的种子'


class MantraUIName():
    def __init__(self, language='en'):
        if language == 'en':

            self.mantra_styles = 'Mantra Styles'
            self.style_name = 'Mantra Name'
            self.style_prompt = 'Mantra Prompt'
            self.style_source = 'Mantra Source'
            self.style_negative_prompt = 'Mantra Negative Prompt'
            self.select_style = 'Selected Mantra'
            self.style_desc = 'Mantra Description'
            self.style_template = 'Mantra Prompt Template'
            self.style_negative_template = 'Mantra Negative Prompt Template'
            self.style_example = 'Mantra Results Example'
            self.style_example_prompt = 'Mantra Example Prompt'

        elif language == 'zh':
            self.mantra_styles = '咒语风格'
            self.style_name = '咒语名称'
            self.style_prompt = '咒语提示'
            self.style_source = '咒语来源'
            self.style_negative_prompt = '咒语负向提示'
            self.select_style = '选定的咒语'
            self.style_desc = '咒语描述'
            self.style_template = '咒语提示模板'
            self.style_negative_template = '咒语负向提示模板'
            self.style_example = '咒语示例图'
            self.style_example_prompt = '咒语示例提示词'


class RefinerUIName():
    def __init__(self, language='en'):
        if language == 'en':

            self.refine_sample = 'Refine Sampler'
            self.refine_discretization = 'Refine Discretization'
            self.refine_guide_scale = 'Refine Guide Scale For Uncondition'
            self.refine_guide_rescale = 'Guide ReScale'
            self.refine_strength = 'Refine Strength'
            self.refine_strength_description = 'Use to control how many steps used to refine.'
            self.refine_diffusion_model = 'Refiner'
            self.refine_cond_model = 'Refine Cond'

        elif language == 'zh':

            self.refine_sample = 'Refine采样器'
            self.refine_discretization = 'Refine离散化'
            self.refine_guide_scale = 'Refine条件引导比例'
            self.refine_guide_rescale = 'Refine引导缩放'
            self.refine_strength = 'Refine强度'
            self.refine_strength_description = '用于控制用于Refine步数。'
            self.refine_diffusion_model = 'Refiner'
            self.refine_cond_model = 'Refine Cond'


class TunerUIName():
    def __init__(self, language='en'):
        if language == 'en':

            self.tuner_model = 'Tuner'
            self.tuner_name = 'Tuner Name'
            self.tuner_type = 'Tuner Type'
            self.tuner_desc = 'Tuner Description'
            self.tuner_example = 'Results Example'
            self.tuner_prompt_example = 'Prompt Example'
            self.base_model = 'Base Model Name'
            self.custom_tuner_model = 'Customized Model'

        elif language == 'zh':
            self.tuner_model = '微调模型'
            self.tuner_name = '微调模型名'
            self.tuner_type = '微调模型类型'
            self.tuner_desc = '微调模型描述'
            self.tuner_example = '示例结果'
            self.tuner_prompt_example = '示例提示词'
            self.base_model = '基础模型'
            self.custom_tuner_model = '自定义模型'


class ControlUIName():
    def __init__(self, language='en'):
        if language == 'en':

            self.source_image = 'Source Image'
            self.cond_image = 'Conditional Image'
            self.control_preprocessor = 'Control Preprocessor'
            self.crop_type = 'Crop type'
            self.direction = (
                "Note: 1) After clicking 'Extract', you can extract "
                'the conditional image from the original image on the left;\n'
                '2) You can also directly transfer the conditional image on the right; \n'
                '3) Or simply upload the original image and directly run the\n'
                "'Conditional Inference' below.")
            self.preprocess = 'Preprocess'
            self.control_model = 'Generation Model'

            self.control_err1 = "Condition preprocessor doesn't exist."
            self.control_err2 = 'Condition preprocessor failed.'
        elif language == 'zh':
            self.preprocess = '条件预处理'
            self.source_image = '源图片'
            self.cond_image = '条件图片'
            self.control_preprocessor = '图像预处理器'
            self.crop_type = '抠图方式'
            self.direction = ('注：1）点击【Extract】后可从左侧原始图像提取出条件图像；\n'
                              '2）也可直接传输右侧条件图像；\n'
                              '3）或只上传原始图像直接运行下方的【条件推理】')
            self.control_err1 = '预处理器不存在。'
            self.control_err2 = '预处理失败。'
            self.control_model = '生成模型'
