import MainBuilderPage from "@/components/builder/mainBuilderPage";

const Builder = async ({searchParams}) => {
    const res = await searchParams
    const tgDataFromServer = res.tgWebAppStartParam;
    return ( 
        <MainBuilderPage initialData={tgDataFromServer}/>
     );
}
 
export default Builder;