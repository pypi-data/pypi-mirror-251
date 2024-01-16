#include "duckdb/function/pragma/pragma_functions.hpp"

#include "duckdb/common/enums/output_type.hpp"
#include "duckdb/common/operator/cast_operators.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/database.hpp"
#include "duckdb/main/query_profiler.hpp"
#include "duckdb/main/secret/secret_manager.hpp"
#include "duckdb/parallel/task_scheduler.hpp"
#include "duckdb/planner/expression_binder.hpp"
#include "duckdb/storage/buffer_manager.hpp"
#include "duckdb/storage/storage_manager.hpp"
#include "duckdb/function/function_set.hpp"

#ifdef LINEAGE
#include "duckdb/main/client_data.hpp"
#endif
#include <cctype>

namespace duckdb {

static void PragmaEnableProfilingStatement(ClientContext &context, const FunctionParameters &parameters) {
	auto &config = ClientConfig::GetConfig(context);
	config.enable_profiler = true;
	config.emit_profiler_output = true;
}

void RegisterEnableProfiling(BuiltinFunctions &set) {
	PragmaFunctionSet functions("");
	functions.AddFunction(PragmaFunction::PragmaStatement(string(), PragmaEnableProfilingStatement));

	set.AddFunction("enable_profile", functions);
	set.AddFunction("enable_profiling", functions);
}

static void PragmaDisableProfiling(ClientContext &context, const FunctionParameters &parameters) {
	auto &config = ClientConfig::GetConfig(context);
	config.enable_profiler = false;
}

static void PragmaEnableProgressBar(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).enable_progress_bar = true;
}

static void PragmaDisableProgressBar(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).enable_progress_bar = false;
}

static void PragmaEnablePrintProgressBar(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).print_progress_bar = true;
}

static void PragmaDisablePrintProgressBar(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).print_progress_bar = false;
}

static void PragmaEnableVerification(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).query_verification_enabled = true;
	ClientConfig::GetConfig(context).verify_serializer = true;
}

static void PragmaDisableVerification(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).query_verification_enabled = false;
	ClientConfig::GetConfig(context).verify_serializer = false;
}

static void PragmaVerifySerializer(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).verify_serializer = true;
}

static void PragmaDisableVerifySerializer(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).verify_serializer = false;
}

static void PragmaEnableExternalVerification(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).verify_external = true;
}

static void PragmaDisableExternalVerification(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).verify_external = false;
}

static void PragmaEnableForceParallelism(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).verify_parallelism = true;
}

static void PragmaForceCheckpoint(ClientContext &context, const FunctionParameters &parameters) {
	DBConfig::GetConfig(context).options.force_checkpoint = true;
}

static void PragmaDisableForceParallelism(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).verify_parallelism = false;
}

static void PragmaEnableObjectCache(ClientContext &context, const FunctionParameters &parameters) {
	DBConfig::GetConfig(context).options.object_cache_enable = true;
}

static void PragmaDisableObjectCache(ClientContext &context, const FunctionParameters &parameters) {
	DBConfig::GetConfig(context).options.object_cache_enable = false;
}

static void PragmaEnableCheckpointOnShutdown(ClientContext &context, const FunctionParameters &parameters) {
	DBConfig::GetConfig(context).options.checkpoint_on_shutdown = true;
}

static void PragmaDisableCheckpointOnShutdown(ClientContext &context, const FunctionParameters &parameters) {
	DBConfig::GetConfig(context).options.checkpoint_on_shutdown = false;
}

static void PragmaEnableOptimizer(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).enable_optimizer = true;
}

static void PragmaDisableOptimizer(ClientContext &context, const FunctionParameters &parameters) {
	ClientConfig::GetConfig(context).enable_optimizer = false;
}

#ifdef LINEAGE
static void PragmaEnableLineage(ClientContext &context, const FunctionParameters &parameters) {
	context.client_data->lineage_manager->trace_lineage = true;
	ClientConfig::GetConfig(context).trace_lineage = true;
	std::cout << "\nEnable Lineage Capture" << std::endl;
}
static void PragmaDisableLineage(ClientContext &context, const FunctionParameters &parameters) {
	context.client_data->lineage_manager->trace_lineage = false;
	ClientConfig::GetConfig(context).trace_lineage = false;
	std::cout << "\nDisable Lineage Capture" << std::endl;
}

static void PragmaEnableIntermediateTables(ClientContext &context, const FunctionParameters &parameters) {
	context.client_data->lineage_manager->persist_intermediate = true;
	std::cout << "\nEnable Intermediate Tables Capture: " << std::endl;
}

static void PragmaDisableIntermediateTables(ClientContext &context, const FunctionParameters &parameters) {
	context.client_data->lineage_manager->persist_intermediate = false;
	std::cout << "\nDisable Intermediate Tables Capture: " << std::endl;
}

static void PragmaEnableKSemimoduleTables(ClientContext &context, const FunctionParameters &parameters) {
	context.client_data->lineage_manager->persist_k_semimodule = true;
	std::cout << "\nEnable K Semimodule Tables Capture: " << std::endl;
}

static void PragmaDisableKSemimoduleTables(ClientContext &context, const FunctionParameters &parameters) {
	context.client_data->lineage_manager->persist_k_semimodule = false;
	std::cout << "\nDisable K Semimodule Tables Capture: " << std::endl;
}

static void PragmaClearLineage(ClientContext &context, const FunctionParameters &parameters) {
	context.client_data->lineage_manager->queryid_to_plan.clear();
	context.client_data->lineage_manager->query_to_id.clear();
	std::cout << "\nClear Lineage" << std::endl;
}
#endif

void PragmaFunctions::RegisterFunction(BuiltinFunctions &set) {
	RegisterEnableProfiling(set);
#ifdef LINEAGE
    set.AddFunction(PragmaFunction::PragmaStatement("enable_lineage", PragmaEnableLineage));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_lineage", PragmaDisableLineage));
	set.AddFunction(PragmaFunction::PragmaStatement("enable_intermediate_tables", PragmaEnableIntermediateTables));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_intermediate_tables", PragmaDisableIntermediateTables));
	set.AddFunction(PragmaFunction::PragmaStatement("enable_k_semimodule_tables", PragmaEnableKSemimoduleTables));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_k_semimodule_tables", PragmaDisableKSemimoduleTables));
	set.AddFunction(PragmaFunction::PragmaStatement("clear_lineage", PragmaClearLineage));
#endif
	set.AddFunction(PragmaFunction::PragmaStatement("disable_profile", PragmaDisableProfiling));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_profiling", PragmaDisableProfiling));

	set.AddFunction(PragmaFunction::PragmaStatement("enable_verification", PragmaEnableVerification));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_verification", PragmaDisableVerification));

	set.AddFunction(PragmaFunction::PragmaStatement("verify_external", PragmaEnableExternalVerification));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_verify_external", PragmaDisableExternalVerification));

	set.AddFunction(PragmaFunction::PragmaStatement("verify_serializer", PragmaVerifySerializer));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_verify_serializer", PragmaDisableVerifySerializer));

	set.AddFunction(PragmaFunction::PragmaStatement("verify_parallelism", PragmaEnableForceParallelism));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_verify_parallelism", PragmaDisableForceParallelism));

	set.AddFunction(PragmaFunction::PragmaStatement("enable_object_cache", PragmaEnableObjectCache));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_object_cache", PragmaDisableObjectCache));

	set.AddFunction(PragmaFunction::PragmaStatement("enable_optimizer", PragmaEnableOptimizer));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_optimizer", PragmaDisableOptimizer));

	set.AddFunction(PragmaFunction::PragmaStatement("force_checkpoint", PragmaForceCheckpoint));

	set.AddFunction(PragmaFunction::PragmaStatement("enable_progress_bar", PragmaEnableProgressBar));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_progress_bar", PragmaDisableProgressBar));

	set.AddFunction(PragmaFunction::PragmaStatement("enable_print_progress_bar", PragmaEnablePrintProgressBar));
	set.AddFunction(PragmaFunction::PragmaStatement("disable_print_progress_bar", PragmaDisablePrintProgressBar));

	set.AddFunction(PragmaFunction::PragmaStatement("enable_checkpoint_on_shutdown", PragmaEnableCheckpointOnShutdown));
	set.AddFunction(
	    PragmaFunction::PragmaStatement("disable_checkpoint_on_shutdown", PragmaDisableCheckpointOnShutdown));
}

} // namespace duckdb
