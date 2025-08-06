<template>
	<div class="icon-wrapper">
		<!-- 返回顶部 -->
		<el-backtop target=".icon-wrapper" :right="100" :bottom="100"/>
		
		<!-- 头部 -->
		<div class="icon-head">
			<h1 class="icon-head_title">Icon 图标库 By D.B.</h1>
			<h4 class="icon-head_txt">
				提供在线图标链接，用于个人NAS设备显示使用，禁止用于商业用途
			</h4>
			<h4 class="icon-head_txt">
				食用方法：左键相应图标即可获取直链！
			</h4>
			<div class="icon-head_stats">
				共 {{ totalCategories }} 个分类 · {{ totalIcons }} 个图标
				<span v-if="currentCategories !== totalCategories">
      · 当前显示 {{ currentCategories }} 个分类 · {{ currentIcons }} 个图标
    </span>
			</div>
			<h4 class="icon-head_txt">
				<a href='https://github.com/DavidBlackCN/my-icons'>Github仓库</a>
			</h4>
			<!--<ul>-->
			<!--	<li>特点：一致的设计风格，高清图标（尺寸：512x512px）。</li>-->
			<!--	<li>使用地点：个人仪表板</li>-->
			<!--	<li>使用方法：单击图标，然后将图标下载到您的设备，然后将其上传到您的仪表板。</li>-->
			<!--	<li>我做了什么：我给它们添加了边框，并重新设计了像素，使它们具有一致的风格和高清晰度（图标来自互联网，版权属于原作者。如果它侵犯了您的权利，请告诉我，我会立即删除它们）。</li>-->
			<!--</ul>-->
			
			<!--<div class="icon-head_switch">-->
			<!--	<el-switch-->
			<!--		v-model="cdnValue"-->
			<!--		inline-prompt-->
			<!--		active-text="CDN"-->
			<!--		inactive-text="域名"-->
			<!--		style="&#45;&#45;el-switch-on-color: #6366f1; &#45;&#45;el-switch-off-color: #ccc"-->
			<!--	/>-->
			<!--</div>-->
		</div>
		
		<!-- 搜索部分 -->
		<div class="icon-search-wrapper">
			<div class="icon-search-content">
				<el-input
					v-model="data.search"
					class="icon-search"
					clearable
					placeholder="搜索图标"
					size="large"
				>
					<!--@keyup.enter="iconSearch"-->
					<template #prepend>
						<el-select
							class="icon-select"
							v-model="data.selectValue"
							placeholder="全部"
							size="large"
							filterable
							clearable
						>
							<!--@change="selectSearch"-->
							<el-option
								v-for="(item, index) in selectData"
								:key="index"
								:label="item.label"
								:value="item.value"
							></el-option>
						</el-select>
					</template>
				</el-input>
			</div>
		</div>
		
		<!-- 图片展示 -->
		<div class="icon-show-wrapper">
			<!-- 外层循环遍历分类 -->
			<div
				class="icon-show-block"
				v-for="(items, category) in data.iconData"
				:key="category"
			>
				<!-- 分类标题 -->
				<div class="icon-show-header">
					<div class="icon-show-header_title">{{ formatCategoryTitle(category) }}</div>
					<div class="icon-show-header_num">{{ items.length }} {{ pluralize(items.length) }}</div>
					<div class="icon-show-header_line"></div>
				</div>
				
				<div class="card">
					<!-- 内层循环遍历当前分类下的项目 -->
					<div
						v-for="item in items"
						:key="item.name"
						class="card_content"
						@click="copyIconUrl(category + '/' + item.name + (item.type === 'svg' ? '.svg' : '.png'))"
					>
						<el-tooltip
							class="item"
							effect="light"
							placement="top"
						>
							<template #content> {{ getItemContent(item) }}</template>
							<!--<template #content>-->
							<el-image
								v-if="item.type === 'svg'"
								class="card_img"
								:src="data.publicPath + 'icon/' + item.name + '.svg'"
								lazy
								fit="contain"
							/>
							<el-image
								v-else
								class="card_img"
								:src="data.publicPath + 'icon/' + category + '/' + item.name + '.png'"
								lazy
								fit="contain"
							/>
						</el-tooltip>
						<div class="card_content_txt" @click="openUrl(item.course)" :class="item.course !== '' ? 'card_content_course' : ''">
							{{ item.name }}
						</div>
					</div>
				</div>
			
			
			</div>
			
			<div v-if="Object.keys(data.iconData).length === 0" class="no-result">
				暂未收录相对应的图标哦 ~~~
			</div>
		</div>
		
		<!-- 页脚 -->
		<div class="icon-footer">
			<p>© 2025.08.06 - Present | By David_Black_</p>
			<p><a href='https://github.com/Siriling/my-icons'>原项目地址</a> — <a href='https://github.com/oliver556/my-icons'>修改版项目</a></p>
		</div>
	
	</div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted, computed } from "vue";
import { ElMessage } from "element-plus";
import clipboard3 from "vue-clipboard3";

export default defineComponent({
	setup() {
		const {toClipboard} = clipboard3();
		const cdnValue = ref(true);
		// 搜索数据
		const data = reactive({
			search: "", // 搜索框的值
			selectValue: "", // 下拉框的值
			publicPath: process.env.BASE_URL,
			get iconData() { // 改为计算属性
				return this.search || this.selectValue ? filteredData.value : rawData.value;
			}
		})
		
		// 下拉框数据
		const selectData = ref<{ label: string; value: string }[]>([]);		// const selectData = reactive([
		
		// 原始数据存储
		const rawData = ref<any>({}); // 新增：存储原始数据

		// 总分类数（所有分类的数量）
		const totalCategories = computed(() => Object.keys(rawData.value).length);

		// 总图标数（所有分类下的图标总数）
		const totalIcons = computed(() => {
			return Object.values(rawData.value).reduce((total: number, items: any) =>
				total + items.length, 0
			);
		});

		// 当前显示分类数（过滤后的分类数量）
		const currentCategories = computed(() => Object.keys(data.iconData).length);

		// 当前显示图标数（过滤后的图标总数）
		const currentIcons = computed(() => {
			return Object.values(data.iconData).reduce((total: number, items: any) =>
				total + items.length, 0
			);
		});

		
		/**
		 * @Description 处理单复数形式
		 */
		const pluralize = (count: number) => {
			return count === 1 ? 'Icon' : 'Icons'
		}
		
		// 修改后的计算属性
		const filteredData = computed(() => {
			const searchTerm = data.search.toLowerCase();
			const selectedCategory = data.selectValue;
			
			return Object.entries(rawData.value).reduce((acc, [category, items]) => {
				// 分类过滤
				if (selectedCategory && category !== selectedCategory) return acc;
				
				// 搜索过滤
				const filteredItems = (items as any[]).filter(item =>
					item.name.toLowerCase().includes(searchTerm)
				);
				
				if (filteredItems.length > 0) {
					acc[category] = filteredItems;
				}
				return acc;
			}, {} as Record<string, any>);
		});
		
		/**
		 * @Description 读取本地图片数据
		 */
		const fetchData = async () => {
			try {
				const response = await fetch('db.json');
				if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
				const jsonData = await response.json();
				
				// 对分类键进行排序
				const sortedCategories = Object.keys(jsonData).sort((a, b) => {
					return a.localeCompare(b, undefined, {
						numeric: true,
						caseFirst: 'upper'
					});
				});
				
				// 对分类下的子类进行排序
				const sortedData: Record<string, any> = {};
				sortedCategories.forEach(category => {
					sortedData[category] = jsonData[category].sort((a, b) => {
						return a.name.localeCompare(b.name, undefined, {
							numeric: true,
							caseFirst: 'upper'
						});
					});
				});
				
				rawData.value = sortedData; // 使用排序后的数据
				selectData.value = extractAndTransformData(sortedData);
			} catch (error) {
				console.error('Error fetching JSON:', error);
			}
		};
		
		/**
		 * @Description 提取并转换数据，给下拉框用的数据
		 */
		const extractAndTransformData = (data) => {
			let extractedData: { label: string; value: string }[] = [];
			
			for (const key in data) {
				if (data.hasOwnProperty(key)) {
					extractedData.push({
						label: key,
						value: key
					});
				}
			}
			return extractedData;
		}
		
		/**
		 * @Description 文图标显示文字提示
		 */
		function getItemContent(item: { name: any; type: string; }) {
			return `${item.name}${item.type === 'svg' ? '.svg' : '.png'}`;
		}
		
		// 分类标题格式化方法
    // 留空弃用
		const formatCategoryTitle = (category) => {
			const titles = {

			};
			return titles[category] || category;
		};
		
		/**
		 * @Description 复制图标链接
		 */
		async function copyIconUrl(url: string) {
			let currenturl = window.location.href;
			let iconurl = data.publicPath + "icon/" + url;
			// let iconurlCdn = "https://cdn.jsdelivr.net/gh/oliver556/my-icons@main/dist/" + "icon/" + url; // CDN Url
			let iconurlCdn = "https://cdn.jsdelivr.net/gh/DavidBlackCN/my-icons@gh-pages/" + "icon/" + url; // CDN Url
			// let iconurlCdn = "https://github.viplee.top/https://raw.githubusercontent.com/oliver556/my-icons/refs/heads/main/dist/icon/" + url; // 套 CF
				
				// 备用 CDN Url
			// fastly.jsdelivr.net
			// gcore.jsdelivr.net
			// testingcf.jsdelivr.net
			
			// 自建 CF 加速转发
			// https://github.viplee.top/https://raw.githubusercontent.com/oliver556/my-icons/refs/heads/main/dist/icon/ + url
			// https://github.viplee.top/https://raw.githubusercontent.com/oliver556/my-icons/refs/heads/main/dist/icon/CMS/Halo_E.png
			let fullurl = currenturl.substr(0, currenturl.length - 2) + iconurl; // 本地 Url
			
			console.log('图片文件全称(url): ', url);
			console.log('当前环境路径(本地) currenturl: ', currenturl);
			console.log('图片文件路径(iconurl): ', iconurl);
			console.log('CDN 拼接后的路径(iconurlCdn): ', iconurlCdn);
			console.log('当前环境拼接后的路径(fullurl): ', fullurl);
			await toClipboard(cdnValue.value ? iconurlCdn : fullurl);
			ElMessage({
				message: "图标链接复制成功",
				type: "success",
			});
		}
		
		/**
		 * @Description 打开相关链接
		 */
		function openUrl(url: string | URL | undefined) {
			window.open(url, "_blank");
		}
		
		onMounted(async () => {
			await fetchData();
		});
		
		return {
			data,
			selectData,
			cdnValue,
			totalCategories,
			totalIcons,
			currentIcons,
			currentCategories,
			pluralize,
			getItemContent,
			formatCategoryTitle,
			copyIconUrl,
			openUrl
		}
	}
})
</script>

<style lang="scss">
/* 颜色变量 */
$primary-color: #6366f1;
$secondary-color: #4f46e5;
$primary-1-color: #0d0f8c;
$secondary-2-color: #1d169c;
$bg-color: #f8fafc;
$text-dark: #1e293b;
$text-light: #64748b;
$white: #fff;
$bg: #F7F9FD;
$bg1: #000000;
$--g0: #1c2226;
$--g1: #4f5d69;
$--g4: #bcc9d2;
$--g5: #e0e6eb;
$--g6: #ecf0f4;
$--g7: #f8fafd;
// 暗黑
$dark-bg: #1a1a1a;
$dark-bg-2: #f0f0f0;
$dark-txt: #d4d4d8;
$dark-txt-2: #333;

* {
	box-sizing: border-box;
	margin: 0;
	padding: 0;
	font-family: 'Inter', system-ui, sans-serif;
}

html, body {
	overflow-x: hidden; // 禁止横向滚动
	max-width: 100vw;
	min-height: 100vh;
	//background: $dark-bg;
}

.icon-wrapper {
	
	display: flex;
	flex-direction: column;
	min-height: 100%;
	//height: 100%;
	overflow: auto; // 防止内容溢出
	position: relative;
	
	// 头部
	.icon-head {
		position: relative;
		padding: 2rem 1.5rem;
		//background: linear-gradient(135deg, $primary-color, $secondary-color);
		//background: linear-gradient(135deg, $primary-1-color, $secondary-2-color);
		background-color: #6aa1b7;
		color: white;
		//box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
		//border-bottom: 1px solid $dark-txt;
		
		&_title {
			font-size: 2.5rem;
			font-weight: 700;
			margin-bottom: 1rem;
			text-align: center;
		}
		
		&_txt {
			font-size: 1rem;
			opacity: 0.9;
			max-width: 800px;
			margin: 0 auto;
			//margin: 0 auto 1rem;
			text-align: center;
		}
		
		&_switch {
			flex-shrink: 0;
			width: auto;
			position: absolute;
			top: 2.8rem;
			right: 1rem;
			
			.el-switch {
				--el-switch-button-size: 20px;
				--el-switch-height: 26px;
			}
		}
		
		
		&_stats {
			text-align: center;
			font-size: 0.9rem;
			color: rgba(255, 255, 255, 0.8);
			margin-bottom: 1rem;
			
			span {
				display: inline-block;
				margin-left: 0.5rem;
				padding-left: 0.5rem;
				border-left: 1px solid rgba(255, 255, 255, 0.3);
			}
			
			@media (max-width: 768px) {
				font-size: 0.8rem;
				span {
					display: block;
					border-left: none;
					margin-left: 0;
					padding-left: 0;
					margin-top: 0.3rem;
				}
			}
		}
	}
	
	// 搜索区域
	.icon-search-wrapper {
		padding: 1.5rem 1.5rem 0;
		display: flex;
		gap: 1rem;
		align-items: center;
		max-width: 1200px;
		margin: 0 auto;
		width: 100%;
		
		//.icon-head_switch {
		//	flex-shrink: 0;
		//	width: auto;
		//
		//	.el-switch {
		//		--el-switch-button-size: 20px;
		//		--el-switch-height: 26px;
		//	}
		//}
		
		.icon-search-content {
			flex: 1;
			min-width: 0;
			
			.el-input {
				//display: flex;
				
				.el-input__inner {
					//background: $dark-bg;
					//color: $dark-txt;
				}
				
				.el-input__wrapper {
					//background-color: $dark-bg;
				}
				
				.el-input-group__prepend {
					//padding: 0;
					//border: none;
					background: transparent;
				}
				
				.el-select {
					//width: auto;
					//min-width: 100px;
					
					.el-input__wrapper {
						//padding: 0 15px;
					}
				}
				
				.el-input__wrapper {
					//border-radius: 8px !important;
				}
			}
		}
		
		@media (max-width: 768px) {
			flex-direction: column;
			padding: 1rem;
			
			.icon-search-wrapper {
				flex-direction: column-reverse;
			}
			
			.icon-search-content {
				width: 100%;
			}
			
			.el-select {
				width: 100% !important;
			}
			
			.el-input {
				.el-input-group__prepend {
					padding: 0;
				}
			}
		}
	}
	
	// 图片展示区域
	.icon-show-wrapper {
		padding: 2rem 1.5rem;
		flex: 1;
		width: 100%;
		overflow: hidden;
		min-height: 100%;
		
		.icon-show-block {
			margin-bottom: 2rem;
			width: 100%;
			background: $bg;
			//border-radius: .75rem;
			padding: 0.5rem 0.5rem 1rem;
			//border: 1px solid #ccc;
			border-radius: 20px;
			
			.icon-show-header {
				margin-bottom: 10px;
				display: flex;
				align-items: center;
				width: 100%;
				flex-wrap: wrap;
				
				> :not(:last-child) {
					margin-right: 10px;
				}
				
				&_title {
					font-weight: 700;
					color: $--g0;
					background-color: $--g6;
					border-radius: 8px;
					padding: 6px 10px;
					margin-bottom: 5px;
				}
				
				&_num {
					font-size: 15px;
					color: $--g1;
					//color: $dark-txt;
					margin-bottom: 5px;
				}
				
				&_line {
					height: 1px;
					flex: 1;
					min-width: 30%;
					background: $--g6;
					margin-bottom: 5px;
				}
			}
			
			.card {
				display: flex;
				flex-wrap: wrap;
				justify-content: flex-start;
				gap: 10px;
				width: 100%;
				
				&_content {
					width: 160px;
					//height: 100px;
					border-radius: 1.5rem;
					// todo
					//background-color: rgba(30, 128, 255, 0.1);
					background-color: #f8f9fa;
					box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
					transition: all 0.3s ease;
					padding: 1rem;
					display: flex;
					flex-direction: column;
					align-items: center;
					justify-content: center;
					cursor: pointer;
					
					&:hover {
						//transform: translateY(-4px);
						//box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
					}
					
					&_txt {
						text-align: center;
						font-size: 0.7rem;
						color: #333;
						font-weight: bold;
					}
				}
				
				.card_content_course {
					color: #79C576;
				}
				
				&_img {
					width: 64px;
					height: 64px;
					margin-bottom: 1rem;
					object-fit: contain;
					transition: all 0.3s ease;
					
					&:hover {
						transform: translateY(-4px);
						border-radius: 13px;
						box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
					}
				}
				
				&_txt {
					font-size: 0.9rem;
					color: $text-light;
					font-weight: 500;
					width: 100%;
					text-align: center;
					white-space: nowrap;
					overflow: hidden;
					text-overflow: ellipsis;
				}
			}
		}
		
		.no-result {
			text-align: center;
			//color: $--g1;
			color: $dark-txt;
			padding: 2rem;
		}
		
		// 移动端适配 图片卡片部分
		@media (max-width: 768px) {
			padding: 0 1rem;
			
			.card {
				justify-content: center;
				gap: 0;
				
				&_content {
					width: calc(21% - 20px);
					height: auto;
					aspect-ratio: 1;
					padding: 0.5rem !important;
					margin: 5px;
				}
				
				&_img {
					width: 56px;
					height: 56px;
				}
			}
			
			.icon-show-header {
				&_title {
					font-size: 0.9rem;
				}
				
				&_num {
					font-size: 0.8rem;
				}
			}
		}
		
		@media (max-width: 480px) {
			.card {
				
				&_content {
					width: calc(33% - 10px);
				}
				
				&_txt {
					font-size: 0.8rem;
				}
			}
		}
	}
}

// Element Plus 组件样式覆盖
.el-select-dropdown {
	.el-select-dropdown__item {
		//white-space: nowrap;
		//overflow: hidden;
		//text-overflow: ellipsis;
		//padding: 0 20px;
	}
}

.icon-footer {
	margin-top: auto; // 关键：自动顶部边距使页脚始终在底部
	padding: 1.5rem;
	text-align: center;
	background: rgba($--g6, 0.8);
	backdrop-filter: blur(5px); // 毛玻璃效果
	border-top: 1px solid $--g5;
	z-index: 10;
	
	p {
		color: $--g1;
		font-size: 0.9rem;
		margin: 0;
		letter-spacing: 0.5px;
		line-height: 1.5;
		
		// 响应式调整
		@media (max-width: 768px) {
			font-size: 0.85rem;
		}
	}
	
	// 动画效果（可选）
	transition: all 0.3s ease;
	
	&:hover {
		background: rgba($--g6, 0.9);
	}
}

// 响应式断点处理
@media (max-width: 1200px) {
	.icon-wrapper {
		.icon-head {
			&_title {
				font-size: 2rem;
			}
			
			//&_txt {
			//	font-size: 0.8rem;
			//}
			
			&_switch {
				top: 2.5rem !important;
				right: 1rem;
			}
		}
	}
}

@media (max-width: 768px) {
	.card {
		gap: 0 !important;
	}
	
	.icon-wrapper {
		.icon-head {
			&_switch {
				top: 2.4rem !important;
				right: 1rem;
			}
		}
	}
}

@media (max-width: 480px) {
	.card {
		gap: 0 !important;
	}
	
	.icon-wrapper {
		.icon-head {
			padding: 1.5rem 1rem;
			
			&_title {
				font-size: 1.5rem;
			}
			
			&_txt {
				font-size: 0.9rem;
				margin: 0 auto;
				//margin: 0 auto 0.5rem;
			}
			
			&_switch {
				top: 1.5rem !important;
				right: 1rem;
			}
		}
	}
}

</style>