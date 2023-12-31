/*
 * @Author: Nya-WSL
 * Copyright © 2023 by Nya-WSL All Rights Reserved. 
 * @Date: 2023-12-31 16:44:14
 * @LastEditors: 狐日泽
 * @LastEditTime: 2023-12-31 17:07:26
 */
export default {
    template: "<div><slot></slot></div>",
    mounted() {
        window.addEventListener("popstate", (event) => {
            if (event.state?.page) {
                this.$emit("open", event.state.page);
            }
        });
        const connectInterval = setInterval(async () => {
            if (window.socket.id === undefined) return;
            this.$emit("open", window.location.pathname);
            clearInterval(connectInterval);
        }, 10);
    },
    props: {},
};